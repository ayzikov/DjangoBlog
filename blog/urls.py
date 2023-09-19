from django.urls import path
from . import views

urlpatterns = [
    # path('', views.list_posts, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.detail_post, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share')
]

app_name = 'blog'