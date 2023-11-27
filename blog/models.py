from taggit.managers import TaggableManager
from slugify import slugify

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Post.Status.PUBLISHED)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model)

    def published(self):
        return self.get_queryset().published()


class Post(models.Model):
    class Meta:
        # установили сортировку по умолчанию (по убыванию для поля publish)
        ordering = ['-publish']
        # установили индексы в БД для поля publish
        indexes = [
            models.Index(fields=['-publish'])
        ]


    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.TextField(max_length=250)

    # unique_for_date означает что поле slug должно быть уникальным для даты в поле publish
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    # related_name позволяет назначать имя атрибуту, который используется для связи от ассоциированного объекта назад к нему.
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)

    tag = TaggableManager(blank=True)


    objects = models.Manager()
    published = PostManager()


    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                             self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug
                             ])
    def __str__(self):
        return self.title

    # Переопределяем функцию save чтобы при сохранении проверялось поле slug и если его нет,
    # то оно добавится автоматически
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    post = models.ForeignKey(to=Post,
                             on_delete=models.CASCADE,
                             related_name='comments')

    name = models.CharField(max_length=40)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
