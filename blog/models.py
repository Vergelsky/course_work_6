from django.db import models

from mailinger.settings import STATIC_URL


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(max_length=3000, verbose_name='Текст')
    image = models.ImageField(upload_to=STATIC_URL/'images', verbose_name='Обложка' )
    datetime = models.DateTimeField(auto_now=True, verbose_name='Когда создан')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    is_published= models.BooleanField(verbose_name='Опубликовано')

