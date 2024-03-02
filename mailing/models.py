from django.db import models


# Create your models here.
class Mailing(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рассылки')
    letter = models.ForeignKey('Letter', on_delete=models.DO_NOTHING, verbose_name='Письмо для рассылки')
    period = models.CharField(max_length=20,
                              choices={'day': 'День', 'week': 'Неделя', 'month': 'Месяц'},
                              verbose_name='Частота рассылки',
                              default='day')
    send_time = models.TimeField(default='12:00:00', verbose_name='Время рассылки')
    is_active = models.BooleanField(default=False, verbose_name='Запущена')
    sends = models.IntegerField(default=0, verbose_name='Отправлено раз')
    clients = models.ManyToManyField(to='Client', verbose_name='Список адресов')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель рассылки', blank=True,
                              null=True)

    def __str__(self):
        return f'{self.name}'


class Log(models.Model):
    last_try_dt = models.DateTimeField(auto_now=True, verbose_name='Время последней рассылки')
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

    def __str__(self):
        return f'Клиент {self.name}'
