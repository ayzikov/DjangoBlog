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

    def save(self, *args, **kwargs):
        ''' Проверяем если фотка больше чем 100 на 100, то делаем ее такой и сохраняем по тому же пути '''
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_size = (100, 100)
            img.thumbnail(new_size)
            img.save(self.avatar.path)
