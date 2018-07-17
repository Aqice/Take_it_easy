from json import JSONDecodeError

from django.http import JsonResponse

from .models import Cafe, Coordinates, Owner, OpeningHours, Item, WaitList

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

import json


@csrf_exempt
def add_cafe(request):
    """

    Функция для добавления нового кафе. POST запрос

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
          - 'cafe_id': ID кафе, информацию которого нужно получить

     return: информация о кафе
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")
    try:
        cafe = Cafe.objects.get(cafe_id=request.GET["cafe_id"])
    except:
        return HttpResponseBadRequest("cafe_id is invalid")

    serialized_obj = serializers.serialize('json', [cafe, ])
    return HttpResponse(serialized_obj)


@csrf_exempt
def remove_cafe(request):
    """

        Функция для удаления кафе. GET запрос

        Параметры:
            - `cafe_id`: ID кафе, которое нужно удалить

        return: 1, если всё прошло штатно
        """
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    try:
        cafe = Cafe.objects.get(cafe_id=request.GET["cafe_id"])
    except:
        return HttpResponseBadRequest("cafe_id is invalid")

    cafe.delete()
    return HttpResponse(1)


@csrf_exempt
def get_cafe_by_coord(request):
    """
    Функция для получения информации о кафе по координатам. GET запрос

    Параметры:
        - 'lat': широта
        - 'lon': долгота
        - 'r': радиус

    return: список `cafe_id`, если всё прошло штатно
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
            - 'cafe_id': ID кафе, координаты которого нужно получить

        return: `coordinates`, если все прошло штатно
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
            - `cafe_id`: ID кафе, владельца которого нужно получить

        return: owner, если все прошло штатно
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
            - `cafe_id`: ID кафе, время работы которого нужно получить

        return: `cafe_opening_hours`, если все прошло штатно
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

        Функция для получения элемента меню кафе по item_id. GET запрос

        Параметры:
            - `item_id`: ID элемента, который нужно получить

        return: информация об элементе меню (`item`), если все прошло штатно
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
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    cafe_json = serializers.serialize("json", Cafe.objects.all())

    return HttpResponse(cafe_json)


@csrf_exempt
def create_new_wait_list(request):
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

    try:
        amounts = json.loads(request.POST["amounts"])
    except KeyError:
        return HttpResponseBadRequest("No amount in request")
    except JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format in amount")
    if len(items) != len(amounts):
        return HttpResponseBadRequest("Lenght of amounts and items are not the same")

    # Сделать по аналогии:
    try:
        client_id = request.POST["client_id"]
        cafe_id = request.POST["cafe_id"]
        time_to_take = request.POST["time_to_take"]
    except Exception:
        return HttpResponseBadRequest("прописать ошибки")

    wait_list = {
        1: WaitList(
            item_1=items[0],
            amount_1=amounts[0],
            client=client_id,
            cafe_id=cafe_id,
            time_to_take=time_to_take,
            paid=False,
            done=False
        ),
        2: WaitList(
            item_1=items[0],
            amount_1=amounts[0],
            item_2=items[1],
            amount_2=amounts[1],
            client=client_id,
            cafe_id=cafe_id,
            time_to_take=time_to_take,
            paid=False,
            done=False
        ),
        3: WaitList(
            item_1=items[0],
            amount_1=amounts[0],
            item_2=items[1],
            amount_2=amounts[1],
            item_3=items[2],
            amount_3=amounts[2],
            client=client_id,
            cafe_id=cafe_id,
            time_to_take=time_to_take,
            paid=False,
            done=False
        ),
        4: WaitList(
            item_1=items[0],
            amount_1=amounts[0],
            item_2=items[1],
            amount_2=amounts[1],
            item_3=items[2],
            amount_3=amounts[2],
            item_4=items[3],
            amount_4=amounts[3],
            client=client_id,
            cafe_id=cafe_id,
            time_to_take=time_to_take,
            paid=False,
            done=False
        ),
        5: WaitList(
            item_1=items[0],
            amount_1=amounts[0],
            item_2=items[1],
            amount_2=amounts[1],
            item_3=items[2],
            amount_3=amounts[2],
            item_4=items[3],
            amount_4=amounts[3],
            item_5=items[4],
            amount_5=amounts[4],
            client=client_id,
            cafe_id=cafe_id,
            time_to_take=time_to_take,
            paid=False,
            done=False
        ),
        6: WaitList(
            item_1=items[0],
            amount_1=amounts[0],
            item_2=items[1],
            amount_2=amounts[1],
            item_3=items[2],
            amount_3=amounts[2],
            item_4=items[3],
            amount_4=amounts[3],
            item_5=items[4],
            amount_5=amounts[4],
            item_6=items[5],
            amount_6=amounts[5],
            client=client_id,
            cafe_id=cafe_id,
            time_to_take=time_to_take,
            paid=False,
            done=False
        ),
    }[len(items)]
    wait_list.save()

    return HttpResponse(wait_list.order_id)


@csrf_exempt
def get_all_wait_lists_by_id(request):
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    # Добавить проверки как в функции ```get_item_by_id```
    wait_list = WaitList.objects.get(order_id=request.GET["wait_list_id"])
    serialized_obj = serializers.serialize('json', [wait_list, ])

    return HttpResponse(serialized_obj)
