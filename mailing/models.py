from django.utils import timezone
from django.db import models

from users.models import User


# Create your models here.
class Mailing(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рассылки')
    letter = models.ForeignKey('Letter', on_delete=models.DO_NOTHING, verbose_name='Письмо для рассылки')
    period = models.CharField(max_length=20,
                              choices={'day': 'День', 'week': 'Неделя', 'month': 'Месяц'},
                              verbose_name='Частота рассылки',
                              default='day')
    start_date = models.DateField(verbose_name='Начало рассылок')
    finish_date = models.DateField(blank=True, null=True, verbose_name='Конец рассылок')
    send_time = models.TimeField(default='12:00:00', verbose_name='Время рассылки')
    status = models.CharField(max_length=50, default='created',
                              choices={'created': 'Создана', 'started': 'Запущена', 'ended': 'Закончена'},
                              verbose_name='Статус')
    sends = models.IntegerField(default=0, verbose_name='Отправлено раз')
    clients = models.ManyToManyField(to='Client', verbose_name='Список адресов')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель рассылки', blank=True,
                              null=True)

    def __str__(self):
        return f'Рассылка {self.name}'


class Log(models.Model):
    last_try_dt = models.DateTimeField(default=timezone.now(), verbose_name='Время последней рассылки')
    result = models.CharField(max_length=600, verbose_name='Результаты выполнения')
    mailing = models.ForeignKey('mailing.Mailing', on_delete=models.CASCADE, verbose_name='Рассылка')


class Letter(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(max_length=1000, verbose_name='Содержимое')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель', blank=True, null=True)

    def __str__(self):
        return f'Письмо {self.name}'


class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name='ФИО')
    about = models.TextField(max_length=600, verbose_name='Комментарий', blank=True)
    email = models.EmailField(unique=True, verbose_name='Почта')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель', blank=True, null=True)

    def __str__(self):
        return f'Клиент {self.name}'
