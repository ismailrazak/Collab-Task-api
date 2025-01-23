import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from house.models import House
from tasks.models import Attachment, Task, TaskList


class TestTaskView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.house1 = mixer.blend(House, name="house1")
        cls.house2 = mixer.blend(House, name="house2")
        cls.user1 = get_user_model().objects.create_user(
            username="test1", password="test", house=cls.house1
        )
        cls.user2 = get_user_model().objects.create_user(
            username="test2", password="test", house=cls.house2
        )

        data1 = {"username": "test1", "password": "test"}
        user1_response = cls.client.post("/api/auth/token/", data=data1)
        access_token_user1 = user1_response.json()["access"]
        data2 = {"username": "test2", "password": "test"}
        user2_response = cls.client.post("/api/auth/token/", data=data2)
        access_token_user2 = user2_response.json()["access"]

        cls.user1_headers = {"Authorization": "Bearer " + access_token_user1}
        cls.user2_headers = {"Authorization": "Bearer " + access_token_user2}
        cls.tasklist1 = mixer.blend(
            TaskList, house=cls.house1, name="tasklist1", created_by=cls.user1
        )
        cls.tasklist2 = mixer.blend(
            TaskList, house=cls.house2, name="tasklist1", created_by=cls.user2
        )

        data_task1 = json.dumps(
            {
                "name": "task1",
                "description": "task1",
                "tasklist": reverse("tasklist-detail", kwargs={"pk": cls.tasklist1.id}),
            }
        )
        response1 = cls.client.post(
            reverse("task-list"),
            data=data_task1,
            headers=cls.user1_headers,
            content_type="application/json",
        )
        cls.task_id = response1.json()["id"]
        assert response1.json()["name"] == "task1"

    def test_task_view(self):
        response = self.client.get(reverse("task-list"), headers=self.user1_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_task_detail_view(self):

        response = self.client.get(
            reverse("task-detail", kwargs={"pk": self.task_id}),
            headers=self.user1_headers,
        )

        assert response.status_code == 200
        assert response.json()["name"] == "task1"

    def test_task_detail_update_completed(self):
        data = {
            "name": "stat",
            "status": "C",
            "tasklist": reverse("tasklist-detail", kwargs={"pk": self.tasklist1.id}),
        }
        response = self.client.put(
            reverse("task-detail", kwargs={"pk": self.task_id}),
            data=data,
            headers=self.user1_headers,
            content_type="application/json",
        )
        assert response.json()["status"] == "C"
        assert response.json()["name"] == "stat"
        assert response.status_code == 200

    def test_task_detail_update_not_completed(self):
        data = {
            "name": "stat",
            "status": "NC",
            "tasklist": reverse("tasklist-detail", kwargs={"pk": self.tasklist1.id}),
        }
        response = self.client.put(
            reverse("task-detail", kwargs={"pk": self.task_id}),
            data=data,
            headers=self.user1_headers,
            content_type="application/json",
        )
        assert response.json()["status"] == "NC"
        assert response.json()["name"] == "stat"
        assert response.status_code == 200

    def test_task_detail_delete(self):

        response = self.client.delete(
            reverse("task-detail", kwargs={"pk": self.task_id}),
            headers=self.user1_headers,
            content_type="application/json",
        )

        assert response.status_code == 204
        response1 = self.client.delete(
            reverse("task-detail", kwargs={"pk": self.task_id}),
            headers=self.user2_headers,
            content_type="application/json",
        )

        assert response1.status_code == 404

    def test_task_post_not_logged_in(self):
        data_task1 = json.dumps(
            {
                "name": "task1",
                "description": "task1",
                "tasklist": reverse(
                    "tasklist-detail", kwargs={"pk": self.tasklist1.id}
                ),
            }
        )
        response1 = self.client.post(
            reverse("task-list"), data=data_task1, content_type="application/json"
        )
        assert response1.status_code == 401
