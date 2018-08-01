import json
from json import JSONDecodeError

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Cafe, Coordinates, Owner, OpeningHours, Item, WaitList, Client


# ToDo Сделать нормальные доки, с примерами выдачи, объяснениями каждого поля в выдаче и на входе

@csrf_exempt
def add_cafe(request):
    """

    **Функция для добавления нового кафе.**
    POST запрос

    Параметры:
        - `owner_name`: ФИО владельца
        - `owner_phone_number`: Телефон владельца
        - `owner_email`: Email владельца
        - `cafe_name`: Название кафе
        - 'cafe_description': Описание кафе
        - 'cafe_rating': Рэйтинг кафе
        - `opening_time`: Время открытия кафе (формат: HH:MM:SS)
        - 'closing_time': Время закрытия кафе (формат: HH:MM:SS)
        - 'lat': Широта кафе
        - 'lon': Долгота кафе

    return: `cafe_id`, если создание прошло успешно
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Incorrect type of request. POST needed.")
    try:
        owner = Owner(
            owner_name=request.POST["owner_name"],
            owner_phone_number=request.POST["owner_phone_number"],
            owner_email=request.POST["owner_email"]
        )
        owner.save()
    except KeyError:
        return HttpResponseBadRequest("Owner information is invalid.")

    try:
        opening_hours = OpeningHours(
            opening_time=request.POST["opening_time"],
            closing_time=request.POST["closing_time"]
        )
        opening_hours.save()
    except KeyError:
        return HttpResponseBadRequest("Opening hours are invalid.")

    try:
        coordinates = Coordinates(
            lat=request.POST["lat"],
            lon=request.POST["lon"]
        )
        coordinates.save()
    except KeyError:
        return HttpResponseBadRequest("Coordinates are invalid.")

    try:
        cafe = Cafe(
            cafe_name=request.POST["cafe_name"],
            cafe_description=request.POST["cafe_description"],
            cafe_rating=request.POST["cafe_rating"],
            cafe_coordinates=coordinates,
            cafe_owner=owner,
            cafe_opening_hours=opening_hours
        )
        cafe.save()
    except KeyError:
        return HttpResponseBadRequest("Cafe information is invalid.")

    return HttpResponse(cafe.cafe_id)


@csrf_exempt
def get_cafe_by_id(request):
    """

    Функция для получение информации о кафе. GET запрос

    Параметры:
      * cafe_id - ID кафе, информацию которого нужно получить

    Возвращаемый словарь:
      * cafe_id - ID кафе
      * cafe_name - Название кафе
      * cafe_description - Описание кафе
      * cafe_rating - Рэйтинг кафе
      * lat - Координата широты кафе
      * lon - Координата долготы кафе
      * cafe_owner - Владелец кафе объект типа :model:`cafes.Owner`, пердставляет словарь с полями:\n
        * owner_id - ID владельца кафе
        * owner_name - Имя владельца кафе
        * owner_phone_number - Номер телефона владельца кафе
        * owner_email - Почта владельца кафе
      * cafe_menu - Мень кафе, список объектов типа :model:`cafes.Item`, где каждый элемент списка словарь с полями:\n
        * item_id - ID продукта
        * item_name - Название продукта
        * item_description - Описание продукта
        * item_time - Время приготовления продукта
        * item_icon - Иконка продукта
        * item_image - Фотография продукта
        * item_cost - Цена продукта
      * cafe_opening_hours - Лист \n
        * нулевой элемент - время открытия кафе
        * первый элемент - время закрытия кафе
      * add_time - Время добавления кафе в систему


    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")
    try:
        cafe = Cafe.objects.get(cafe_id=request.GET["cafe_id"])
    except:
        return HttpResponseBadRequest("cafe_id is invalid")

    return HttpResponse(json.dumps(cafe.to_dict()))


@csrf_exempt
def remove_cafe(request):
    """

        Функция для удаления кафе. POST запрос

        Параметры:
            - `cafe_id`: ID кафе, которое нужно удалить

        return: 1, если всё прошло штатно
        """
    if request.method != "POST":
        return HttpResponseBadRequest("Incorrect type of request. POST needed.")

    try:
        cafe = Cafe.objects.get(cafe_id=request.GET["cafe_id"])
    except:
        return HttpResponseBadRequest("cafe_id is invalid")

    cafe.delete()
    return HttpResponse(1)


@csrf_exempt
def get_cafe_by_coord(request):
    """
    Функция для получения информации ID ближайших кафе по координатам. GET запрос

    Параметры:
      * lat - широта
      * lon - долгота
      * r - радиус

    Возвращает:
      * список `cafe_id`

    Для получения полной информации о кафе нужно воспользоваться функцией :view:`cafes.views.get_cafe_by_id`
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    try:
        lat = int(request.GET["lat"])
        lon = int(request.GET["lon"])
        r = int(request.GET["r"])
    except KeyError:
        return HttpResponseBadRequest("lat, lon or r parameter is invalid")

    r2 = r ** 2

    all_cafes = Cafe.objects.all()
    id_of_cafes_in_circle = []

    for cafe in all_cafes:
        if (cafe.cafe_coordinates.lat - lat) ** 2 + (cafe.cafe_coordinates.lon - lon) ** 2 <= r2:
            id_of_cafes_in_circle.append(cafe.cafe_id)

    return HttpResponse(json.dumps(id_of_cafes_in_circle))


@csrf_exempt
def get_coord_by_id(request):
    """

        Функция для получения координат кафе по cafe_id. GET запрос

        Параметры:
          * cafe_id - ID кафе, координаты которого нужно получить

        Возвращает:
          * Объект :model:`cafes.Coordinates`
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    try:
        coordinates = Coordinates.objects.get(coordinates_id=int(request.GET["id"]))
    except:
        return HttpResponseBadRequest("id is invalid")

    serialized_obj = serializers.serialize('json', [coordinates, ])

    return HttpResponse(serialized_obj)


def get_owner_by_id(request):
    """

        Функция для получения владельца кафе по cafe_id. GET запрос

        Параметры:
          * cafe_id - ID кафе, владельца которого нужно получить

        Возвращает:
          * Объект :model:`cafes.Owner`
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    try:
        owner = Owner.objects.get(owner_id=int(request.GET["id"]))
    except KeyError:
        return HttpResponseBadRequest("id is invalid")

    serialized_obj = serializers.serialize('json', [owner, ])

    return HttpResponse(serialized_obj)


@csrf_exempt
def get_cafe_opening_hours_by_id(request):
    """

        Функция для получения времени работы кафе по cafe_id. GET запрос

        Параметры:
          * cafe_id - ID кафе, время работы которого нужно получить

        Возвращает:
         * Объект :model:`cafes.OpeningHours`
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    try:
        cafe_opening_hours = OpeningHours.objects.get(opening_hours_id=int(request.GET["id"]))
    except:
        return HttpResponseBadRequest("id is invalid")

    serialized_obj = serializers.serialize('json', [cafe_opening_hours, ])

    return HttpResponse(serialized_obj)


@csrf_exempt
def get_item_by_id(request):
    """

        Функция для получения продукта по его ID. GET запрос

        Параметры:
          * item_id - ID элемента, который нужно получить

        Возвращает:
          * Объект :model:`cafes.Item`
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    try:
        item = Item.objects.get(item_id=int(request.GET["id"]))
    except KeyError:
        return HttpResponseBadRequest("No id in request")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("No object with your id")

    serialized_obj = serializers.serialize('json', [item, ])

    return HttpResponse(serialized_obj)


@csrf_exempt
def get_all_cafes(request):
    """

        Функция для получения списка всех ID

        Параметры отсутсвуют

        Возвращает:
          * Список ID объектов :model:`cafes.Cafe`
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    cafe_json = serializers.serialize("json", Cafe.objects.all())

    return HttpResponse(cafe_json)


@csrf_exempt
def create_new_wait_list(request):
    """

        Функция для создания нового списка ожидания для кафе

        Параметры:
            - блюда (`items`) массив в json
            - количества каждого блюда (`amounts`) массив в json
            - id клиента (`client_id`)
            - id кафе (`cafe_id`)
            - время, к которому необходимо приготовить заказ (`time_to_take`) в формате xx.yy.zz

        return: номер заказа (`order_id`), если все прошло штатно
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Incorrect type of request. POST needed.")

    try:
        items = json.loads(request.POST["items"])
    except KeyError:
        return HttpResponseBadRequest("No items in request")
    except JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format in items")
    if len(items) > 6:
        return HttpResponseBadRequest("Too many items. Maximum is 6")
    if len(items) < 1:
        return HttpResponseBadRequest("No items.")

    try:
        amounts = json.loads(request.POST["amounts"])
    except KeyError:
        return HttpResponseBadRequest("No amount in request")
    except JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format in amount")
    if len(items) != len(amounts):
        return HttpResponseBadRequest("Length of amounts and items are not the same")

    try:
        client_id = request.POST["client_id"]
    except KeyError:
        return HttpResponseBadRequest("No client_id in request")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("No object with your id")

    try:
        cafe_id = request.POST["cafe_id"]
        # как поведет себя этот метод, если для кафе с таким cafe_id уже существует waitlist?
    except KeyError:
        return HttpResponseBadRequest("No id in request")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("No object with your id")

    try:
        time_to_take = request.POST["time_to_take"]
    except KeyError:
        return HttpResponseBadRequest("Bad time format")

    if len(items) == 1:
        wait_list = WaitList(
            item_1=Item.objects.get(item_id=items[0]),
            amount_1=amounts[0],
            client=Client.objects.get(client_id=client_id),
            cafe_id=Cafe.objects.get(cafe_id=cafe_id),
            time_to_take=time_to_take,
            paid=False,
            done=False
        )
    elif len(items) == 2:
        wait_list = WaitList(
            item_1=Item.objects.get(item_id=items[0]),
            amount_1=amounts[0],
            item_2=Item.objects.get(item_id=items[1]),
            amount_2=amounts[1],
            client=Client.objects.get(client_id=client_id),
            cafe_id=Cafe.objects.get(cafe_id=cafe_id),
            time_to_take=time_to_take,
            paid=False,
            done=False
        )
    elif len(items) == 3:
        wait_list = WaitList(
            item_1=Item.objects.get(item_id=items[0]),
            amount_1=amounts[0],
            item_2=Item.objects.get(item_id=items[1]),
            amount_2=amounts[1],
            item_3=Item.objects.get(item_id=items[2]),
            amount_3=amounts[2],
            client=Client.objects.get(client_id=client_id),
            cafe_id=Cafe.objects.get(cafe_id=cafe_id),
            time_to_take=time_to_take,
            paid=False,
            done=False
        )
    elif len(items) == 4:
        wait_list = WaitList(
            item_1=Item.objects.get(item_id=items[0]),
            amount_1=amounts[0],
            item_2=Item.objects.get(item_id=items[1]),
            amount_2=amounts[1],
            item_3=Item.objects.get(item_id=items[2]),
            amount_3=amounts[2],
            item_4=Item.objects.get(item_id=items[3]),
            amount_4=amounts[3],
            client=Client.objects.get(client_id=client_id),
            cafe_id=Cafe.objects.get(cafe_id=cafe_id),
            time_to_take=time_to_take,
            paid=False,
            done=False
        )
    elif len(items) == 5:
        wait_list = WaitList(
            item_1=Item.objects.get(item_id=items[0]),
            amount_1=amounts[0],
            item_2=Item.objects.get(item_id=items[1]),
            amount_2=amounts[1],
            item_3=Item.objects.get(item_id=items[2]),
            amount_3=amounts[2],
            item_4=Item.objects.get(item_id=items[3]),
            amount_4=amounts[3],
            item_5=Item.objects.get(item_id=items[4]),
            amount_5=amounts[4],
            client=Client.objects.get(client_id=client_id),
            cafe_id=Cafe.objects.get(cafe_id=cafe_id),
            time_to_take=time_to_take,
            paid=False,
            done=False
        )
    elif len(items) == 6:
        wait_list = WaitList(
            item_1=Item.objects.get(item_id=items[0]),
            amount_1=amounts[0],
            item_2=Item.objects.get(item_id=items[1]),
            amount_2=amounts[1],
            item_3=Item.objects.get(item_id=items[2]),
            amount_3=amounts[2],
            item_4=Item.objects.get(item_id=items[3]),
            amount_4=amounts[3],
            item_5=Item.objects.get(item_id=items[4]),
            amount_5=amounts[4],
            item_6=Item.objects.get(item_id=items[5]),
            amount_6=amounts[5],
            client=Client.objects.get(client_id=client_id),
            cafe_id=Cafe.objects.get(cafe_id=cafe_id),
            time_to_take=time_to_take,
            paid=False,
            done=False
        )

    wait_list.save()

    return HttpResponse(wait_list.order_id)


@csrf_exempt
def get_all_wait_lists_by_cafe_id(request):
    """

        Функция для получения списка заказов по `cafe_id`

        Параметры:
            - `cafe_id`: ID кафе, список заказов которого нужно получить

        return: список из заказов (`WaitList`), если все прошло штатно
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")
    try:
        wait_list = WaitList.objects.get(
            cafe_id=request.GET["cafe_id"],
            done=False
        )
    except KeyError:
        return HttpResponseBadRequest("No id in request")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("No object with your id")
    serialized_obj = serializers.serialize('json', [wait_list, ])

    return HttpResponse(serialized_obj)


@csrf_exempt
def change_wait_list_paid_status(request):
    """

        Функция для изменения статуса done у объекта WaitList по `wait_list_id`

        Параметры:
            - `wait_list_id`: ID WaitList, статус которого нужно изменить

        return: Новый статус объекта WaitList, если всё прошло штатно
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Incorrect type of request. POST needed.")

    try:
        wait_list = WaitList.objects.get(
            order_id=request.POST["wait_list_id"]
        )
    except KeyError:
        return HttpResponseBadRequest("No wait_list_id in request")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("No WaitList object with this ID")
    if wait_list.done:
        return HttpResponseBadRequest("WaitList object done status already is True")

    wait_list.done = True
    wait_list.save()
    return HttpResponse(wait_list.done)


@csrf_exempt
def add_new_client(request):
    """

       Функция для добавления нового клиента. POST запрос

       Параметры:
           - `client_id`: id клиента(id чата в телеграме)
           - `first_name`: Имя
           - `second_name`: Фамилия
           - `patronymic`: Отчество
           - 'phone_number': Номер телефона клиента
        Возвращает:
            ID созданнаго клиентау
       """
    if request.method != "POST":
        return HttpResponseBadRequest("Incorrect type of request. POST needed.")
    try:
        client = Client(
            client_id=request.POST["client_id"],
            first_name=request.POST["first_name"],
            second_name=request.POST["second_name"],
            patronymic=request.POST["patronymic"],
            phone_number=request.POST["phone_number"]
        )

    except KeyError as e:
        return HttpResponseBadRequest("No " + e.args[0][1:-1] + " in request")

    client.save()
    return HttpResponse(client.client_id)


@csrf_exempt
def check_user_in_database(request):
    """

       Функция для регестрации пользователя. GET запрос

       Параметры:
           - `client_id`: id клиента(id чата в телеграме)
       Возвращает:
           True -- клиент зарегестрирован,
           False -- клиент не зарегестрирован
       """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. POST needed.")
    try:
        client_id = request.GET["client_id"]
    except KeyError:
        return HttpResponseBadRequest("No client_id in request")

    return HttpResponse(Client.objects.filter(client_id=client_id).exists())
