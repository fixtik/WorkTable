from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from todolist.models import Todolist
from . import serializers


class TodoistListApiView(APIView):
    """
    Представление, которое позволяет вывести весь список дел и добавить новую запись.
    Выводит записи всех пользователей, вне зависимости от статуса, публичности и т.д.
    работа через url: cases
    """

    def get(self, request: Request) -> Response:
        """Вывод всех дел"""
        if not IsAuthenticated:  # Отбрасываем всех неавторизованных
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        objects = Todolist.objects.all()
        serializer = serializers.TodolistSerializer(
            instance=objects,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request: Request):
        """Добавление записи через json"""
        if not IsAuthenticated:  # Отбрасываем всех неавторизованных
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.TodolistSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class TodoOnceView(APIView):
    """
    Представление для работы с единичной записью
    Доступ к записи - по ключу, работа через url: case/int
    """
    def get(self, request: Request, pk: int) -> Response:
        """Отображение заданной записи по заданному ключу"""
        if not IsAuthenticated:  # Отбрасываем всех неавторизованных
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = get_object_or_404(Todolist, pk=pk)  # проверка наличия записи по указанному ключу
        serializer = serializers.TodolistSerializer(instance=queryset)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Response:
        """Полное обновление записи по ключу"""
        if not IsAuthenticated:  # Отбрасываем всех неавторизованных
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = get_object_or_404(Todolist, pk=pk)

        if queryset.author.username != request.user:  # запрещаем пользователю изменять чужие заметки
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.TodolistSerializer(instance=queryset,   # объект с которым работаем
                                                    data=request.data,   # данные из браузера
                                                    partial=True)        # разрешение передавать часть объектов
        if serializer.is_valid(True):  # проверка данных с разрешением вызова исключений
            serializer.save()  # сохранение данных
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    def patch(self, request:Request, pk: int) -> Response:
        """Частичное обновление записи по ключу"""
        return self.put(request, pk)


class TaskListCreateAPIView(generics.ListCreateAPIView):
    """представление через generic """
    queryset = Todolist.objects.all()
    serializer_class = serializers.TodolistSerializer

    ordering = ["important", "update_at"]  # поля для сортировки

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.order_by_queryset(queryset)
        return queryset

    def order_by_queryset(self, queryset):
        """
        Сортировка заметок по дате, затем по важности.
        """
        return queryset.order_by(*self.ordering)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # добавили автора для сохранения


class TodoPublicListApiView(generics.ListAPIView):
    """
    Представление для отображения только публичных записей для
    авторизованных пользователей, сортировка по времени
    """
    queryset = Todolist.objects.all()
    serializer_class = serializers.TodolistSerializer
    permission_classes = (IsAuthenticated,)  # запрещаем неавторизованных пользователей

    def get_queryset(self):

        queryset = super().get_queryset()
        return queryset.filter(public=True).order_by("-create_at")


