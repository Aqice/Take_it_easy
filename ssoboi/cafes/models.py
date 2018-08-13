from django.db import models
import django.utils.timezone
from django.contrib.auth.models import User
from users.models import User


class Coordinates(models.Model):
    coordinates_id = models.AutoField(
        primary_key=True,
        verbose_name="id координат"
    )

    lat = models.FloatField(
        verbose_name="Широта",
    )
    lon = models.FloatField(
        verbose_name="Долгота",
    )

    def __str__(self):
        return "Широта: " + str(self.lat) + " Долгота:" + str(self.lon)

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon


class Owner(models.Model):
    owner_id = models.AutoField(
        primary_key=True,
        verbose_name="ID владельца",
    )
    owner_name = models.CharField(
        verbose_name="ФИО владельца",
        max_length=1000,
    )
    owner_phone_number = models.TextField(
        verbose_name="Телефон владельца",
    )
    owner_email = models.TextField(
        verbose_name="Email владельца",
    )

    def __str__(self):
        return self.owner_name

    def to_dict(self):
        return {
            "owner_id": self.owner_id,
            "owner_name": self.owner_name,
            "owner_phone_number": self.owner_phone_number,
            "owner_email": self.owner_email
        }


class Item(models.Model):
    item_id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        verbose_name="Название элемента",
        max_length=1000,
    )
    description = models.TextField(
        verbose_name="Описание элемента"
    )
    time = models.IntegerField(
        verbose_name="Время приготовления (в минутах)",
        default=10
    )
    icon = models.ImageField(
        verbose_name="Иконка элемента",
        blank=True
    )
    image = models.ImageField(
        verbose_name="Фото элемента",
        blank=True
    )
    price = models.IntegerField(
        verbose_name="Цена товара"
    )
    type = models.CharField(
        verbose_name="Тип товара",
        max_length=100
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

    def get_opening_hours(self):
        return [str(self.opening_time), str(self.closing_time)]


class Feedback(models.Model):
    feedback_id = models.AutoField(
        primary_key=True
    )
    author = models.OneToOneField(
        User,
        verbose_name="Автор отзыва",
        on_delete=models.CASCADE
    )
    desc = models.CharField(
        verbose_name="Отзыв",
        max_length=3500
    )
    rating = models.FloatField(
        verbose_name="Рейтинг отзыва",
    )
    add_time = models.DateTimeField(
        verbose_name="Дата добавления",
        default=django.utils.timezone.now
    )

    def __str__(self):
        return "feedback by", str(self.author), "(" + str(self.add_time) + ")"


class Cafe(models.Model):
    # ToDo сделать отдельное поле для отзывов, связать с объектом кафе и клиента
    # ToDo сделать функцию для изменения рейтинга кафе(встроить в функцию добавления отзыва)
    # ToDo добавить картинки для кафе
    cafe_id = models.AutoField(
        primary_key=True,
        verbose_name="ID кафе",
    )
    cafe_name = models.CharField(
        verbose_name="Название кафе",
        max_length=1000,
        default=" "
    )
    cafe_description = models.CharField(
        verbose_name="Описание кафе",
        max_length=1000,
    )
    cafe_rating = models.FloatField(
        verbose_name="Рейтинг кафе",
    )
    cafe_coordinates = models.ForeignKey(
        Coordinates,
        on_delete=models.CASCADE,
        verbose_name="Координаты кафе",
    )
    cafe_owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        verbose_name="Владелец кафе",
    )
    cafe_menu = models.ManyToManyField(
        Item,
        verbose_name="Меню",
    )
    cafe_opening_hours = models.ForeignKey(
        OpeningHours,
        on_delete=models.CASCADE,
        verbose_name="Часы работы кафе"
    )
    add_time = models.DateTimeField(
        verbose_name='Дата добавления',
        default=django.utils.timezone.now
    )
    cafe_staff = models.ManyToManyField(
        User,
        verbose_name='Работники кафе'
    )
    icon = models.ImageField(
        # Иконка кафе (типа как буква М у макдака), если кафе не имеет такого логотипа,
        # то поставим какой-нибудь стандартный
        verbose_name="Иконка кафе",
        default=None
        # ToDo организация нескольких картинок кафе (manyToMany, либо как-то еще)
        # Смысла делать отдельно класс cafeMedia пока не вижу
    )
    cafe_feedback = models.ManyToManyField(
        Feedback,
        verbose_name="Отзывы о кафе",
        blank=True
    )



    def __str__(self):
        return self.cafe_name

    def to_dict(self):
        cafe_menu = []
        for item in (self.cafe_menu.all()):
            temp = item.__dict__
            del temp["_state"]
            cafe_menu.append(temp)

        dict_for_return = {
            "cafe_id": self.cafe_id,
            "cafe_name": self.cafe_name,
            "cafe_description": self.cafe_description,
            "cafe_rating": self.cafe_rating,
            "lon": self.cafe_coordinates.get_lon(),
            "lat": self.cafe_coordinates.get_lat(),
            "cafe_owner": self.cafe_owner.to_dict(),
            "cafe_menu": cafe_menu,
            "cafe_opening_hours": self.cafe_opening_hours.get_opening_hours(),
            "add_time": str(self.add_time)
        }
        return dict_for_return


# ToDo Переписать, выглядит крайне погано, подумать, как лучше сделать
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
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Клиент",
    )
    cafe_id = models.ForeignKey(
        Cafe, verbose_name="Кафе", on_delete=models.CASCADE
    )

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
