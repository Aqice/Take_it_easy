from .models import Cafe, Coordinates, Owner, OpeningHours

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

@csrf_exempt
def add_cafe(request):
    """
    Функция для добавления нового кафе

    :param request: POST запрос, включающий в себя:
                        owner_name - ФИО владельца
                        owner_phone_number - телефон фладельца
                        owner_email - email владельца
                        cafe_name - название кафе
                        cafe_description - описание кафе
                        cafe_rating - рэйтинг кафе
                        opening_time - время открытия кафе (формат: HH:MM:SS)
                        closing_time - время закрытия кафе (формат: HH:MM:SS)
                        lat - Широта кафе
                        lon - Долгота кафе


    :return: ID созданного кафе, если все параметры указаны верно
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

    Функция для получение информации о кафе

    :param request: GET запрос, включающий в себя:
                        cafe_id - ID кафе, информацию которого нужно получить
    :return: информация о кафе
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

        Функция для удаления кафе

        :param request: GET запрос, включающий в себя:
                            cafe_id - ID кафе, которое нужно удалить
        :return: 1, если всё прошло штатно
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
    if request.method != "GET":
        return HttpResponseBadRequest("Incorrect type of request. GET needed.")

    try:
        lat = int(request.GET["lat"])
        lon = int(request.GET["lon"])
        r = int(request.GET["r"])
    except KeyError:
        return HttpResponseBadRequest("lat, lon or r parameter is invalid")

    r2 = r**2

    all_cafes = Cafe.objects.all()
    id_of_cafes_in_circle = []

    for cafe in all_cafes:
        if (cafe.cafe_coordinates.lat - lat) ** 2 + (cafe.cafe_coordinates.lon - lon) ** 2 <= r2:
            id_of_cafes_in_circle.append(cafe.cafe_id)

    return HttpResponse(json.dumps(id_of_cafes_in_circle))
