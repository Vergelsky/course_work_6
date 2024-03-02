# Generated by Django 5.0.2 on 2024-02-28 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('text', models.TextField(max_length=1000, verbose_name='Содержимое')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_try_dt', models.DateTimeField(auto_now=True, verbose_name='Время последней рассылки')),
                ('result', models.CharField(max_length=600, verbose_name='Результаты выполнения')),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рассылки')),
                ('period', models.CharField(choices=[('day', 'День'), ('week', 'Неделя'), ('month', 'Месяц')], default='day', max_length=20, verbose_name='Частота рассылки')),
                ('send_time', models.TimeField(auto_now=True, verbose_name='Время рассылки')),
                ('is_active', models.BooleanField(default=False, verbose_name='Запущена')),
                ('sends', models.IntegerField(default=0, verbose_name='Отправлено раз')),
                ('emails', models.TextField(max_length=3000, verbose_name='Список адресов')),
            ],
        ),
    ]