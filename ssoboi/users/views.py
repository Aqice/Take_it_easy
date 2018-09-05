from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class UserReg(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        """
        Функция для регистрации нового пользователя

        Параметры:
          * username - Имя пользователя. Должно быть уникальным
          * email - Email пользователя. Должен быть уникальным
          * first_name - Имя пользователя
          * last_name - Фамилия пользователя

        Возвращает:
          username, если пользователь был создан, иначе ошибку
        """
        try:
            user = User.objects.create_user(
                username=request.POST["username"],
                email=request.POST["email"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                password=request.POST["password"]
            )
        except KeyError as e:
            return Response("No " + e.args[0] + " field", status=400)
        except IntegrityError as e:
            return Response(e.args[0], status=400)
        return Response(user.username, status=201)


class UserAuth(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError as e:
            return Response("No " + e.args[0] + " field", status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=200)
        else:
            return Response("User not found", status=400)


class UserlLogOut(APIView):

    permission_classes = (permissions.AllowAny, permissions.IsAuthenticated)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        logout(request)
        return Response(status=200)
