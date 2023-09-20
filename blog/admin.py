from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    # определяет какие поля отображаются в админ-панели
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    # определяет боковую панель с полями по которым можно включить фильтрацию
    list_filter = ['status', 'created', 'publish', 'author']
    # определяет поля по которым ведется поиск в админ-панели
    search_fields = ['title', 'body', 'author__username']
    # при добавлении нового поста поле slug будет заполняться автоматически
    prepopulated_fields = {'slug': ('title',)}
    # при добавлении поста поле автора теперь будет не выпадающим списком, а полем для поиска
    raw_id_fields = ['author']
    # ссылки для навигации по датам
    date_hierarchy = 'publish'
    # все посты будут автоматически сортироваться по статусу и по дате публикации
    ordering = ['status', 'publish']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['id', 'name', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']