from PIL import Image

# импорты джанго
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ''' Модель профиля пользователя '''

    # связь один к одному с моделью пользователя
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

