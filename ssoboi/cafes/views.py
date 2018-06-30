from datetime import time
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Cafe, Coordinates, Owner, OpeningHours
from django.views.decorators.csrf import csrf_exempt


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
                        opening_time - время открытия кафе
                        closing_time - время закрытия кафе
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
            # opening_time=request.POST["opening_time"],
            # closing_time=request.POST["closing_time"]
            opening_time=(time(hour=6, minute=0, second=0, microsecond=0, tzinfo=None)),
            closing_time=(time(hour=22, minute=0, second=0, microsecond=0, tzinfo=None))
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
