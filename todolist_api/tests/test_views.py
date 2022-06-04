from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from todolist.models import Todolist

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
        # users = [
        #     User(**cls.USER_1),
        #     User(**cls.USER_2),
        # ]
        # User.objects.bulk_create(users)
        # Добавление пользователей в БД
        db_user_1 = User(**cls.USER_1)
        db_user_1.save()
        cls.db_user_1 = db_user_1
        db_user2 = User(**cls.USER_2)
        db_user2.save()
        # добавление записей
        tasks = [
             Todolist(title="title_1", author=cls.db_user_1),
             Todolist(title="title_2", author=db_user2),
             Todolist(title="title_public_true", author=db_user2, public=True),
             Todolist(title="title_public_false", author=db_user2, public=False),
         ]
        Todolist.objects.bulk_create(tasks)

        # добавление проверяемых url
        cls.url_list = [
            f"/api/v1/cases/",  # все записи через generic
            f"/api/v1/all_cases",  # все записи через apiview
            f"/api/v1/case/",  # проверка TodoOnceView
            f"/api/v1/edit_case/"  # проверка edit via generic
        ]

    def setUp(self) -> None:
        """При каждом тестовом методе, будем делать нового клиента и авторизовать его."""
        self.auth_user_1 = APIClient()
        self.an_auth_user = APIClient()
        self.auth_user_1.force_authenticate(user=self.db_user_1)  # так как не интересуют сами механизмы авторизации, авторизуем нашего пользователя принудительно

    def test_get_all_case(self):
        """
        Проверка двух представлений на вывод всех записей авторизованным пользователям
        """
        for url in self.url_list[:2]:
            resp = self.auth_user_1.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_all_case_unautorization(self):
        """
        Проверка на доступ неавторизованным пользователям
        """
        for url in self.url_list[:2]:
            resp = self.an_auth_user.get(url)
            self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_get(self):
        """
        Проверка двух get представлений:
        TodoOnceView и TodoEditViaGeneric
        """
        task_pk = 1 # user1, public
        for url in self.url_list[2:4]:
            resp = self.auth_user_1.get(url+str(task_pk))
            self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_partial_update_other_task(self):
        """проверка изменения чужих записей"""
        task_pk = 2  # user2, public
        for url in self.url_list[2:4]:
            resp = self.auth_user_1.patch(url + str(task_pk))
            self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_delete_other_task(self):
        """проверка удаления чужих записей"""
        task_pk = 2  # user2, public
        for url in self.url_list[2:4]:
            resp = self.auth_user_1.delete(url + str(task_pk))
            self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_other_task(self):
        data = {
            "title": "fake_title",
        }
        task_pk = 2  # user2, public
        for url in self.url_list[2:4]:
            resp = self.auth_user_1.put(url + str(task_pk), data=data)
            self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_prived_case(self):
        """проверка на доступ к приватной записи иного лица"""
        task_pk = 4
        for url in self.url_list[2:4]:
            resp = self.auth_user_1.get(url + str(task_pk))
            self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
