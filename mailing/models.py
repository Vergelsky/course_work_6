from django.db import models

from users.models import User


# Create your models here.
class Mailing(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рассылки')
    letter = models.ForeignKey('Letters', on_delete=models.DO_NOTHING, verbose_name='Письмо для рассылки')
    period = models.CharField(max_length='20',
                              choices={'day': 'День', 'week': 'Неделя', 'month': 'Месяц'},
                              verbose_name='Частота рассылки',
                              default='day')
    send_time = models.TimeField(auto_now=True, verbose_name='Время рассылки')
    sends = models.IntegerField(default=0, verbose_name='Отправлено раз')
    emails = models.TextField(max_length=3000, verbose_name='Список адресов')
    owner = models.ForeignKey('User', on_delete=models.CASCADE(), verbose_name='Создатель рассылки')


class Log(models.Model):
    last_try_dt = models.DateTimeField(auto_now=True, verbose_name='Время последней рассылки')
    result = models.CharField(max_length=600, verbose_name='Результаты выполнения')
    maling = models.ForeignKey('Mailing', on_delete=models.CASCADE(), verbose_name='Рассылка')


class Letter(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(max_length=1000, verbose_name='Содержимое')
    owner = models.ForeignKey('User', on_delete=models.CASCADE(), verbose_name='Создатель')
