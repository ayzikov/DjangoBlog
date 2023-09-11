from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)


    def __str__(self):
        return self.title