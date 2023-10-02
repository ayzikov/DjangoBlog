import markdown

from ..models import Post

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count_posts=5):
    latest_posts = Post.published.all().order_by('-publish')[:count_posts]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/post/most_commented_posts.html')
def get_most_commented_posts(count=5):
    most_commented_posts = Post.published.annotate(total_comments=Count('comments')
                                                   ).order_by('-total_comments')[:count]
    return {'most_commented_posts': most_commented_posts}



@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter
def pluralize_ru(value, arg="пост,поста,постов"):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]