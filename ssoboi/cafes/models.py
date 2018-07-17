from django.db import models
import django.utils.timezone


class Coordinates(models.Model):
    coordinates_id = models.AutoField(
        primary_key=True,
    )

    lat = models.FloatField(
        verbose_name="Широта",
    )
    lon = models.FloatField(
        verbose_name="Долгота",
    )

    def __str__(self):
        return "Широта: " + str(self.lat) + " Долгота:" + str(self.lon)


class Owner(models.Model):
    owner_id = models.AutoField(
        primary_key=True, verbose_name="ID владельца",
    )
    owner_name = models.CharField(
        verbose_name="ФИО владельца", max_length=1000,
    )
    owner_phone_number = models.TextField(
        verbose_name="Телефон владельца",
    )
    owner_email = models.TextField(
        verbose_name="Email владельца",
    )

    def __str__(self):
        return self.owner_name


class CafeMedia(models.Model):
    media_id = models.AutoField(
        primary_key=True,
    )
    icon = models.ImageField(
        verbose_name="Иконка кафе"
    )
    photos = models.ImageField(
        verbose_name="Картинки кафе"
    )
    cafe_id = models.IntegerField(
        verbose_name="ID кафе"
    )


class Item(models.Model):
    item_id = models.AutoField(
        primary_key=True
    )
    item_name = models.CharField(
        verbose_name="Название элемента", max_length=1000,
    )
    item_description = models.TextField(
        verbose_name="Описание элемента"
    )
    item_time = models.IntegerField(
        verbose_name="Время приготовления (в минутах)",
        default=10
    )
    item_icon = models.ImageField(
        verbose_name="Иконка элемента",
        blank=True
    )
    item_image = models.ImageField(
        verbose_name="Фото элемента",
        blank=True
    )

    def __str__(self):
        return str(self.item_name) + ' - ' + str(self.item_description)


class WaitList(models.Model):
    order_id = models.AutoField(
        primary_key=True
    )
    item_1 = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='item_1', null=True
    )
    amount_1 = models.IntegerField(
        verbose_name="Количество", default=1
    )

    item_2 = models.ForeignKey(
        Item, verbose_name="Продукт 2", on_delete=models.CASCADE, blank=True, related_name='item_2', null=True
    )
    amount_2 = models.IntegerField(
        verbose_name="Количество", blank=True, null=True
    )

    item_3 = models.ForeignKey(
        Item, verbose_name="Продукт 3", on_delete=models.CASCADE, blank=True, related_name='item_3', null=True
    )
    amount_3 = models.IntegerField(
        verbose_name="Количество", blank=True, null=True
    )

    item_4 = models.ForeignKey(
        Item, verbose_name="Продукт 4", on_delete=models.CASCADE, blank=True, related_name='item_4', null=True
    )
    amount_4 = models.IntegerField(
        verbose_name="Количество", blank=True, null=True
    )

    item_5 = models.ForeignKey(
        Item, verbose_name="Продукт 5", on_delete=models.CASCADE, blank=True, related_name='item_5', null=True
    )
    amount_5 = models.IntegerField(
        verbose_name="Количество", blank=True, null=True
    )

    item_6 = models.ForeignKey(
        Item, verbose_name="Продукт 6", on_delete=models.CASCADE, blank=True, related_name='item_6', null=True
    )
    amount_6 = models.IntegerField(
        verbose_name="Количество", blank=True, null=True
    )
# TODO: Client class
#    client = models.ForeignKey(
#       Client, on_delete=models.CASCADE, verbose_name="Заказчик",
#    )
    time_to_take = models.TimeField(
        verbose_name="Заказ будет готов к "
    )
    paid = models.BooleanField(
        verbose_name="Оплачено"
    )
    done = models.BooleanField(
        verbose_name="Готовность заказа"
    )

    def __str__(self):
        return 'Заказ №' + str(self.order_id) + " (Готов к " + str(self.time_to_take)[:-3] + ")"


class OpeningHours(models.Model):
    opening_hours_id = models.AutoField(
        primary_key=True,
    )
    opening_time = models.TimeField(
        verbose_name="Время открытия"
    )
    closing_time = models.TimeField(
        verbose_name="Время закрытия"
    )

    def __str__(self):
        return str(self.opening_time) + " -- " + str(self.closing_time)


class Cafe(models.Model):
    cafe_id = models.AutoField(
        primary_key=True, verbose_name="ID кафе",
    )
    cafe_name = models.CharField(
        verbose_name="Название кафе", max_length=1000, default=" "
    )
    cafe_description = models.CharField(
        verbose_name="Описание кафе", max_length=1000,
    )
    cafe_rating = models.FloatField(
        verbose_name="Рейтинг кафе",
    )
    cafe_coordinates = models.ForeignKey(
        Coordinates, on_delete=models.CASCADE, verbose_name="Координаты кафе",
    )
    cafe_owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, verbose_name="Владелец кафе",
    )
    cafe_menu = models.ManyToManyField(
        Item,
        verbose_name="Меню",
    )
    # cafe_waitList = models.ForeignKey(
    #     WaitList,
    #     verbose_name="Список заказов",
    #     on_delete=models.CASCADE,
    #     null=True
    # )
    cafe_opening_hours = models.ForeignKey(
        OpeningHours, on_delete=models.CASCADE, verbose_name="Часы работы кафе"
    )
    add_time = models.DateTimeField(verbose_name='Дата добавления', default=django.utils.timezone.now)

    def __str__(self):
        return self.cafe_name
