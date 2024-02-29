# Generated by Django 5.0.2 on 2024-02-28 10:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mailing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='letter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mailing.letter', verbose_name='Письмо для рассылки'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель рассылки'),
        ),
        migrations.AddField(
            model_name='log',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Рассылка'),
        ),
    ]
