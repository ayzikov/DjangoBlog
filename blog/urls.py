from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_posts, name='post_list'),
    path('tags/<slug:tag_slug>/', views.list_posts, name='post_list_tag_filter'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/get/', views.detail_post, name='post_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.detail_post, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/<int:user_id>/comment/', views.post_comment, name='post_comment'),
    path('search/', views.post_search, name='post_search'),
]

app_name = 'blog'