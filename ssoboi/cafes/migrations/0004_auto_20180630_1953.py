# Generated by Django 2.0.6 on 2018-06-30 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0003_auto_20180630_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='cafe_menu',
            field=models.ManyToManyField(related_name='cafe_menu', to='cafes.Item'),
        ),
    ]
