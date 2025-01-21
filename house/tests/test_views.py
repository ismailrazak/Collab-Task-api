from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from six import assertRaisesRegex

from house.models import House


class TestHouseView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.house = mixer.blend(House, name="test_house")
        cls.client = APIClient()

        cls.manager = get_user_model().objects.create_user(
            username="test", password="test"
        )
        data = {"username": "test", "password": "test"}
        manager_response = cls.client.post("/api/auth/token/", data=data)
        access_token_manager = manager_response.json()["access"]
        cls.manger_headers = {"Authorization": "Bearer " + access_token_manager}

        house_data = {
            "name": "house1",
            "description": "house1",
        }
        cls.house_response = cls.client.post(
            reverse("house-list"), data=house_data, headers=cls.manger_headers
        )
        cls.house_id = cls.house_response.json()["id"]

        cls.member = get_user_model().objects.create_user(
            username="test_member", password="test"
        )
        data2 = {"username": "test_member", "password": "test"}
        member_response = cls.client.post("/api/auth/token/", data=data2)
        member_access_token = member_response.json()["access"]
        cls.member_headers = {"Authorization": "Bearer " + member_access_token}

    def test_house_list_view(self):
        test_client = APIClient()
        response1 = test_client.get(reverse("house-list"))
        response2 = self.client.get(reverse("house-list"), headers=self.manger_headers)
        assert response1.status_code == 401
        assert len(response2.json()) == 2
        assert response2.status_code == 200

    def test_house_detail_read(self):
        response = self.client.get(
            reverse("house-detail", kwargs={"pk": self.house.pk}),
            headers=self.manger_headers,
        )
        assert response.json()["name"] == "test_house"
        assert response.status_code == 200

    def test_house_detail_update_manager(self):
        data = {"name": "house2", "description": "house2"}
        response = self.client.put(
            reverse("house-detail", kwargs={"pk": self.house_id}),
            data=data,
            headers=self.manger_headers,
            content_type="application/json",
        )
        assert response.json()["name"] == "house2"
        assert response.status_code == 200

    def test_house_detail_update_member(self):
        data = {"name": "test"}
        response3 = self.client.put(
            reverse("house-detail", kwargs={"pk": self.house_id}),
            data=data,
            headers=self.member_headers,
            content_type="application/json",
        )
        assert response3.status_code == 403

    def test_house_detail_delete_manager(self):
        response = self.client.delete(
            reverse("house-detail", kwargs={"pk": self.house_id}),
            headers=self.manger_headers,
            content_type="application/json",
        )
        assert response.status_code == 204

    def test_house_detail_delete_member(self):
        response = self.client.delete(
            reverse("house-detail", kwargs={"pk": self.house_id}),
            headers=self.member_headers,
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_house_detail_join_action_manager(self):
        response = self.client.post(
            f"/api/houses/houses/{self.house_id}/join/",
            content_type="application/json",
            headers=self.manger_headers,
        )
        assert response.status_code == 400
        response1 = self.client.post(
            f"/api/houses/houses/{self.house_id}/join/", content_type="application/json"
        )
        assert response1.status_code == 500
        assert response.json()["info"] == "user is already a member of the house."

    def test_house_detail_join_action_member(self):
        response = self.client.post(
            f"/api/houses/houses/{self.house_id}/join/",
            content_type="application/json",
            headers=self.member_headers,
        )
        assert response.status_code == 200
        assert (
            response.json()["info"] == "user has been added to the house successfully."
        )

    def test_house_detail_leave_member(self):
        test_response = self.client.post(
            f"/api/houses/houses/{self.house_id}/join/",
            content_type="application/json",
            headers=self.member_headers,
        )
        response = self.client.post(
            f"/api/houses/houses/{self.house_id}/leave/",
            content_type="application/json",
            headers=self.member_headers,
        )
        assert response.status_code == 200
        assert response.json()["info"] == "user has left the house successfully."
        response1 = self.client.post(
            f"/api/houses/houses/{self.house_id}/leave/",
            content_type="application/json",
            headers=self.member_headers,
        )
        response3 = self.client.post(
            f"/api/houses/houses/{123}/leave/", content_type="application/json"
        )
        assert response1.status_code == 400
        assert response1.json()["info"] == "user is not a member of the house."
        assert response3.json()["error"] == "error while leaving."

    def test_house_manager_leave(self):
        data = {"name": "testhouse", "description": "testhouse"}
        test_response = self.client.post(
            reverse("house-list"), headers=self.member_headers, data=data
        )
        house_id = test_response.json()["id"]
        response = self.client.post(
            f"/api/houses/houses/{house_id}/leave/",
            content_type="application/json",
            headers=self.member_headers,
        )

        assert response.status_code == 200

    def test_house_detail_remove_member(self):
        test_response = self.client.post(
            f"/api/houses/houses/{self.house_id}/join/",
            content_type="application/json",
            headers=self.member_headers,
        )
        data = {"user": self.member.id}
        response = self.client.post(
            f"/api/houses/houses/{self.house_id}/remove/",
            content_type="application/json",
            headers=self.manger_headers,
            data=data,
        )

        assert response.json()["info"] == "user has been removed successfully."
        assert response.status_code == 200
        data1 = {"user": 123}

        response1 = self.client.post(
            f"/api/houses/houses/{self.house_id}/remove/",
            content_type="application/json",
            headers=self.manger_headers,
            data=data1,
        )

        assert response1.status_code == 500
