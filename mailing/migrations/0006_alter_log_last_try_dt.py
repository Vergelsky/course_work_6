# Generated by Django 5.0.2 on 2024-03-03 19:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_remove_mailing_is_active_mailing_finish_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='last_try_dt',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 19, 44, 49, 674619, tzinfo=datetime.timezone.utc), verbose_name='Время последней рассылки'),
        ),
    ]
