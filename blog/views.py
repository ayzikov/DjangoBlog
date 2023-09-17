from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import HttpRequest
from django.core.paginator import Paginator
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
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list_posts.html'


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



