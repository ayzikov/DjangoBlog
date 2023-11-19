from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    Функция вызывается каждый раз при сохранении нового пользователя в БД
    :param sender:
    :param instance: экземпляр модели User который был сохранен
    :param created: bool значение, True==объект создан только что
    '''
    if created:
        # если пользователь создан только что, создается новый объект Profile
        prof = Profile.objects.create(user=instance)
        # Созданному пользователю присваивается автоматически сгенерированный токен
        Token.objects.create(user=instance)
        prof.save()



@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    ''' Функция вызывается каждый раз при изменении профиля и сохраняет его '''
    instance.profile.save()