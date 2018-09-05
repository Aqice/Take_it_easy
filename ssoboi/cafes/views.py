import json

from rest_framework import permissions
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from .models import Cafe, Item, Order
from .serializers import CafeSerializer, OrderSerializer
from users.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class CafeList(APIView):
    def get(self, request):
        """
        Получение листа всех кафе
        """
        cafe_queryset = Cafe.objects.all()
        serializer = CafeSerializer(cafe_queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class CafeDetail(APIView):
    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise Http404

    def get(self, request, pk):
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
        try:
            cafe = self.get_object(pk)
        except Http404:
            return HttpResponse(status=404)

        serializer = CafeSerializer(cafe)
        return JsonResponse(serializer.data)


@csrf_exempt
def get_cafe_by_name(request):
    try:
        cafes = Cafe.objects.get(cafe_name=request.GET["cafe_name"])
    except Cafe.DoesNotExist:
        return HttpResponse(status=404)
    except MultiValueDictKeyError:
        return HttpResponse(status=400)

    if request.method == "GET":
        if type(cafes) == Cafe:
            serializer = CafeSerializer(cafes)
        else:
            serializer = CafeSerializer(cafes, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_cafe_by_coord(request):
    """
    Функция для получения информации ID ближайших кафе по координатам. GET запрос

    Параметры:
      * lat - широта
      * lon - долгота
      * r - радиус

    Возвращает:
      * список словарей, в каждом из которых есть следующие ключи\n
        * cafe_id - ID объекта :model:`cafes.Cafe`
        * cafe_lat - Координата широты кафе
        * cafe_lon - Координата долготы кафе

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
    cafes = []
    for cafe in all_cafes:
        if (cafe.cafe_coordinates.lat - lat) ** 2 + (cafe.cafe_coordinates.lon - lon) ** 2 <= r2:
            cafes.append(
                {
                    "icon": cafe.icon.url,
                    "cafe_name": cafe.cafe_name,
                    "cafe_coordinates": {
                        "lat": cafe.cafe_coordinates.lat,
                        "lon": cafe.cafe_coordinates.lon
                    },
                    "cafe_description": cafe.cafe_description,
                    "cafe_id": cafe.cafe_id
                }
            )

    return JsonResponse(cafes, safe=False)


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


class OrdersList(APIView):
    def get(self, request):
        try:
            cafe_id = request.GET["cafe_id"]
        except KeyError as e:
            return Response("No " + e.args[0] + " field", status=400)

        order_queryset = Order.objects.filter(
            cafe_id=cafe_id,
            taken=False
        )
        serializer = OrderSerializer(order_queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class OrderCreation(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        try:
            customer = User.objects.get(username=request.user)
            on_time = request.POST["on_time"]
            item_id = request.POST["items"]
            cafe_id = request.POST["cafe_id"]
        except KeyError as e:
            return Response("No " + e.args[0] + " field", status=400)
        order = Order(
            customer=customer,
            on_time=on_time,
            items=Item.objects.get(item_id=item_id),
            cafe_id=Cafe.objects.get(cafe_id=cafe_id)
        )
        order.save()
        return Response(status=200)


class ChangingOrderStatus(APIView):
    def post(self, request):
        try:
            order_id = request.data["order_id"]
            status_type = request.data["status_type"]
        except KeyError as e:
            return Response("No " + e.args[0] + " field", status=400)

        try:
            order = Order.objects.get(
                id=order_id
            )
        except Exception as e:
            return Response("No " + e.args[0] + " field", status=400)

        if status_type == "done":
            order.done = True
        elif status_type == "taken":
            order.taken = True
        else:
            return Response("Bad status_type", status=400)
        order.save()
        return Response(status=200)
