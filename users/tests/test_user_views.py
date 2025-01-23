from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient


class TestUserViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        data = {
            "first_name": "test",
            "last_name": "test",
            "email": "test@gmail.com",
            "password": "test",
        }
        response_user = cls.client.post(reverse("user-list"), data=data)
        cls.user_id = response_user.json()["id"]
        assert response_user.status_code == 201

        data = {"username": "test_test", "password": "test"}
        _response = cls.client.post("/api/auth/token/", data=data)

        access_token = _response.json()["access"]
        cls.user_headers = {"Authorization": "Bearer " + access_token}

    def test_user_password_update(self):
        data = {
            "first_name": "ismail",
            "last_name": "razak",
            "email": "test@gmail.com",
            "password": "test",
            "new_password": "test1",
        }

        response = self.client.put(
            reverse("user-detail", kwargs={"pk": self.user_id}),
            data=data,
            headers=self.user_headers,
            content_type="application/json",
        )

        assert response.status_code == 200

        response1 = self.client.put(
            reverse("user-detail", kwargs={"pk": self.user_id}),
            data=data,
            content_type="application/json",
        )

        assert response1.status_code == 401
