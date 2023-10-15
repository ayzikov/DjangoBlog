# импорты проекта
from .models import Post
from .forms import EmailPostForm, CommentPostForm, SearchForm
from taggit.models import Tag

# импорты джанго
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


def list_posts(request: HttpRequest, tag_slug=None):
    posts = Post.published.published()

    tag = None
    if tag_slug:
        # если передали slug тега, то получаем его экзепляр и в posts
        # получаем QuerySet постов у которых в тегах есть такой тег
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tag__in=[tag])


    # реализация постраничной разбивки
    paginator = Paginator(posts, 3)
    # получаем из параметров url номер страницы, если этого параметра нет, то получаем 1
    page_number = request.GET.get('page', 1)
    # получаем объект Page, который содержит посты на странице page_number
    page_obj = paginator.get_page(page_number)

    return render(request,
                  'blog/post/list_posts.html',
                  {'page_obj': page_obj, 'tag': tag})

# class PostListView(ListView):
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list_posts.html'
#     queryset = Post.published.all()


def detail_post(request: HttpRequest, year, month, day, slug):
    ''' Функция извлекает либо объект из БД либо вызывает исключение 404 '''
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug)

    # сортировка комментариев
    comment_order = 'created'
    if 'desc' in request.GET:
        comment_order = '-created'
    elif 'asc' in request.GET:
        comment_order = 'created'
    comments = post.comments.filter(active=True).order_by(comment_order)

    # форма для комментариев
    form = CommentPostForm()

    # выборка постов с одинаковыми тегами

    # список id тегов которые есть у данного поста (post), flat=True чтобы получить [1, 2, 3, ...],
    # а не [(1,), (2,), (3,), ...]
    post_tags = post.tag.values_list('id', flat=True)

    # получаем QS (QuerySet) постов с тегами которые содержат id такие же как и у данного поста (post)
    # например: если у поста 3 одинаковых тега с данным постом (post), то он добавляется в QS 3 раза
    # исключаем из этого QS данный пост (post)
    similar_posts = Post.published.filter(tag__in=post_tags).exclude(id=post.id)

    # с помощью annotate добавляем к каждому объекту QS новое поле same_tags,
    # которое содержит количество одинаковых тегов с данным постом (post) и сортируем
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})

def post_share(request: HttpRequest, post_id):
    ''' Функция для вывода формы и отправки email '''
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    sent = False

    # проверяем тип запроса и выводим форму либо отправляем сообщение на почту
    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        # проверяем входные данные в форме
        if form.is_valid():
            # словарь полей формы и их значений
            cd = form.cleaned_data

            # абсолютный url поста
            post_url = request.build_absolute_uri(post.get_absolute_url())

            # тема сообщения
            email_title = f"Новый пост"

            # тело сообщения
            email_body = (f"Пользователь {cd['name']} поделился с Вами постом\n'{post.title}'\n\n"
                          f"Прочитать можно по этой ссылке - {post_url}\n\n"
                          f"Комментарий пользователя:\n"
                          f"{cd['comment']}")

            send_mail(
                subject=email_title,
                message=email_body,
                from_email='ayzikov070@yandex.ru',
                recipient_list=[cd['to_email']]
            )

            sent = True



    else:
        form = EmailPostForm()

    return render(request,
                  'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request: HttpRequest, post_id):
    ''' Представление для создания комментариев '''

    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    comment = None

    # получаем экземпляр формы с данными которые ввел пользователь
    form = CommentPostForm(request.POST)

    if form.is_valid():
        # создаем объект комментария не сохраняя его в БД
        comment = form.save(commit=False)

        # добавляем пост к комментарию
        comment.post = post

        # сохраняем в БД
        comment.save()


    return render(request,
                  'blog/post/comment.html',
                  {'post': post, 'form': form, 'comment': comment}
                  )


def post_search(request: HttpRequest):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_query = SearchQuery(query, config='russian')
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')

            # почему то без этой строки не работает следующая 😐
            test = Post.published.get(id=3)

            # записываем в словарь все QS в у которых в одном из полей (title или body) было найдено слово (query)
            # results = ((Post.published.
            #            annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).
            #            filter(rank__gte=0.3)).
            #            order_by('-rank'))

            results = ((Post.published.
                       annotate(similarity=TrigramSimilarity('title', query)).
                       filter(similarity__gte=0.1)).
                       order_by('-similarity'))

    return render(request,
                  'blog/post/search.html',
                  {'form': form, 'query': query, 'results': results})





