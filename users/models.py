from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта')
    username = models.CharField(max_length=80, unique=True, verbose_name='Имя пользователя')
    about = models.CharField(max_length=600, verbose_name='О себе', blank=True, null=True)
    is_manager = models.BooleanField(default=False, verbose_name='Это менеджер')
    verification_code = models.CharField(max_length=50, verbose_name='код верификации пользователя', null=True, blank=True)

