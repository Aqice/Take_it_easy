# Generated by Django 2.0.6 on 2018-07-14 11:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0006_auto_20180714_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 14, 11, 59, 22, 533993, tzinfo=utc), verbose_name='Дата добавления'),
        ),
    ]
