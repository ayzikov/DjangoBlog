# импорты проекта
from .models import Post
from .forms import EmailPostForm

# импорты джанго
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

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
    # функция извлекает либо объект из БД либо вызывает исключение 404
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug)


    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

def post_share(request: HttpRequest, post_id):
    ''' Функция для вывода формы и отправки email '''
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    # проверяем тип запроса и выводим форму либо отправляем сообщение на почту
    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        # проверяем входные данные в форме
        if form.is_valid():
            # словарь полей формы и их значений
            cd = form.cleaned_data
            return HttpResponse('<h1>Форма валидна</h1>')

    else:
        form = EmailPostForm()
        return render(request,
                      'blog/post/share.html',
                      {'post': post, 'form': form})

