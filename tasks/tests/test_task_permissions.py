import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from pre_commit.commands.migrate_config import migrate_config
from rest_framework.test import APIClient

from tasks.models import TaskList


class TestTaskListPermission(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user1 = get_user_model().objects.create_user(
            username="test1", password="test"
        )
        data1 = {"username": "test1", "password": "test"}
        user1_response = cls.client.post("/api/auth/token/", data=data1)
        access_token_user1 = user1_response.json()["access"]
        cls.user1_headers = {"Authorization": "Bearer " + access_token_user1}
        cls.tasklist = mixer.blend(TaskList)

    def test_tasklist_has_permission_method(self):

        response = self.client.post(reverse("tasklist-list"))
        assert response.status_code == 401

    def test_tasklist_has_object_permission_method(self):

        response = self.client.get(
            reverse("tasklist-detail", kwargs={"pk": self.tasklist.id})
        )
        assert response.status_code == 401
