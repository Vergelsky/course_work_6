from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта')
    name = models.CharField(unique=True, verbose_name='Имя пользователя')
    about = models.CharField(blank=True, null=True, verbose_name='О себе')
    is_manager = models.BooleanField(default=False, verbose_name='Это менеджер')
