# импорты проекта
from .models import Post
from .forms import EmailPostForm, CommentPostForm

# импорты джанго
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


# def list_posts(request: HttpRequest):
#     posts = Post.published.published()
#     paginator = Paginator(posts, 3)
#
#     # получаем из параметров url номер страницы, если этого параметра нет, то получаем 1
#     page_number = request.GET.get('page', 1)
#     # получаем объект Page, который содержит посты на странице page_number
#     page_obj = paginator.get_page(page_number)
#
#     return render(request,
#                   'blog/post/list_posts.html',
#                   {'page_obj': page_obj})

class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list_posts.html'
    queryset = Post.published.all()


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

    form = CommentPostForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'form': form})

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








