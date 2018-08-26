import json
from json import JSONDecodeError

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from .models import Cafe, Owner, Item, WaitList
from .serializers import CafeSerializer
from users.models import User


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
        print(pk)
        try:
            snippet = self.get_object(pk)
        except Http404:
            return HttpResponse(status=404)

        serializer = CafeSerializer(snippet)
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
            cafes.append(cafe)

    serializer = CafeSerializer(cafes, many=True)

    return JsonResponse(serializer.data, safe=False)


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
def create_new_wait_list(request):
    """

        Функция для создания нового списка ожидания для кафе

        Параметры:
            - блюда (`items`) массив в json
            - количества каждого блюда (`amounts`) массив в json
            - id клиента (`User_id`)
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
        User_id = request.POST["User_id"]
    except KeyError:
        return HttpResponseBadRequest("No User_id in request")
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
            User=User.objects.get(User_id=User_id),
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
            User=User.objects.get(User_id=User_id),
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
            User=User.objects.get(User_id=User_id),
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
            User=User.objects.get(User_id=User_id),
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
            User=User.objects.get(User_id=User_id),
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
            User=User.objects.get(User_id=User_id),
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
