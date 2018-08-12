# Generated by Django 2.1 on 2018-08-12 11:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('cafe_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID кафе')),
                ('cafe_name', models.CharField(default=' ', max_length=1000, verbose_name='Название кафе')),
                ('cafe_description', models.CharField(max_length=1000, verbose_name='Описание кафе')),
                ('cafe_rating', models.FloatField(verbose_name='Рейтинг кафе')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата добавления')),
            ],
        ),
        migrations.CreateModel(
            name='CafeMedia',
            fields=[
                ('media_id', models.AutoField(primary_key=True, serialize=False)),
                ('icon', models.ImageField(upload_to='', verbose_name='Иконка кафе')),
                ('photos', models.ImageField(upload_to='', verbose_name='Картинки кафе')),
                ('cafe_id', models.IntegerField(verbose_name='ID кафе')),
            ],
        ),
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('coordinates_id', models.AutoField(primary_key=True, serialize=False, verbose_name='id координат')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('lon', models.FloatField(verbose_name='Долгота')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=1000, verbose_name='Название элемента')),
                ('item_description', models.TextField(verbose_name='Описание элемента')),
                ('item_time', models.IntegerField(default=10, verbose_name='Время приготовления (в минутах)')),
                ('item_icon', models.ImageField(blank=True, upload_to='', verbose_name='Иконка элемента')),
                ('item_image', models.ImageField(blank=True, upload_to='', verbose_name='Фото элемента')),
                ('item_cost', models.IntegerField(verbose_name='Цена товара')),
                ('item_type', models.CharField(max_length=100, verbose_name='Тип товара')),
            ],
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('opening_hours_id', models.AutoField(primary_key=True, serialize=False)),
                ('opening_time', models.TimeField(verbose_name='Время открытия')),
                ('closing_time', models.TimeField(verbose_name='Время закрытия')),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('owner_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID владельца')),
                ('owner_name', models.CharField(max_length=1000, verbose_name='ФИО владельца')),
                ('owner_phone_number', models.TextField(verbose_name='Телефон владельца')),
                ('owner_email', models.TextField(verbose_name='Email владельца')),
            ],
        ),
        migrations.CreateModel(
            name='WaitList',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount_1', models.IntegerField(default=1, verbose_name='Количество')),
                ('amount_2', models.IntegerField(blank=True, null=True, verbose_name='Количество')),
                ('amount_3', models.IntegerField(blank=True, null=True, verbose_name='Количество')),
                ('amount_4', models.IntegerField(blank=True, null=True, verbose_name='Количество')),
                ('amount_5', models.IntegerField(blank=True, null=True, verbose_name='Количество')),
                ('amount_6', models.IntegerField(blank=True, null=True, verbose_name='Количество')),
                ('time_to_take', models.TimeField(verbose_name='Заказ будет готов к ')),
                ('paid', models.BooleanField(verbose_name='Оплачено')),
                ('done', models.BooleanField(verbose_name='Готовность заказа')),
                ('cafe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafes.Cafe', verbose_name='Кафе')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='Клиент')),
                ('item_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_1', to='cafes.Item')),
                ('item_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_2', to='cafes.Item', verbose_name='Продукт 2')),
                ('item_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_3', to='cafes.Item', verbose_name='Продукт 3')),
                ('item_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_4', to='cafes.Item', verbose_name='Продукт 4')),
                ('item_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_5', to='cafes.Item', verbose_name='Продукт 5')),
                ('item_6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_6', to='cafes.Item', verbose_name='Продукт 6')),
            ],
        ),
        migrations.AddField(
            model_name='cafe',
            name='cafe_coordinates',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafes.Coordinates', verbose_name='Координаты кафе'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='cafe_menu',
            field=models.ManyToManyField(to='cafes.Item', verbose_name='Меню'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='cafe_opening_hours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafes.OpeningHours', verbose_name='Часы работы кафе'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='cafe_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafes.Owner', verbose_name='Владелец кафе'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='cafe_staff',
            field=models.ManyToManyField(to='users.User', verbose_name='Работники кафе'),
        ),
    ]
