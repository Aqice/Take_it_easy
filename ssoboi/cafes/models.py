from django.db import models


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
    item_icon = models.ImageField(
        verbose_name="Иконка элемента"
    )
    item_image = models.ImageField(
        verbose_name="Фото элемента"
    )

    def __str__(self):
        return str(self.item_name) + ' - ' + str(self.item_description)


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
        Item
    )
    cafe_opening_hours = models.ForeignKey(
        OpeningHours, on_delete=models.CASCADE, verbose_name="Часы работы кафе"
    )

    def __str__(self):
        return self.cafe_name
