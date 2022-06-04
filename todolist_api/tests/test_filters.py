from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from todolist.models import Todolist
from todolist_api import filtres

User = get_user_model()


class TestTaskRetrieveUpdateDestroyAPIView(APITestCase):
    USER_1 = dict(
        username="username_1",
        password="fake_password",
    )
    USER_2 = dict(
        username="username_2",
        password="fake_password",
    )

    @classmethod
    def setUpTestData(cls):
        """
        Делаем двух пользователей в БД.
        Каждому из них назначаем по записи.
        """
        # Добавление пользователей в БД
        db_user_1 = User(**cls.USER_1)
        db_user_1.save()
        cls.db_user_1 = db_user_1
        db_user2 = User(**cls.USER_2)
        db_user2.save()
        # добавление записей
        tasks = [
             Todolist(title="title_1", author=cls.db_user_1, important=False),
             Todolist(title="title_2", author=db_user2, important=True),
             Todolist(title="title_public_true", author=db_user2, public=True),
             Todolist(title="title_public_false", author=db_user2, public=False),
         ]
        Todolist.objects.bulk_create(tasks)
        cls.queryset = Todolist.objects.all()

    def test_filters_by_public(self):
        """проверка фильтра по публичности"""
        public_case = False  # отбираем все приватные записи

        excpected_queryset = Todolist.objects.filter(public=False)
        actual_queryset = filtres.filter_by_public(self.queryset, public_case)
        self.assertQuerysetEqual(excpected_queryset, actual_queryset, ordered=False)

    def test_filters_by_important(self):
        """проверка фильтра по важности"""
        important = True  # отбираем все важные
        excpected_queryset = Todolist.objects.filter(important=True)
        actual_queryset = filtres.filter_by_important(self.queryset, important)
        self.assertQuerysetEqual(excpected_queryset, actual_queryset, ordered=False)

    def test_filters_by_status(self):
        """проверка фильтра по статусу"""
        status = [1,2]
        excpected_queryset = Todolist.objects.filter(status__in=status)
        actual_queryset = filtres.filter_by_status(self.queryset, status)
        self.assertQuerysetEqual(excpected_queryset, actual_queryset, ordered=False)