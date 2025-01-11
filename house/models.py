import os.path
import uuid

from django.conf import settings
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class GenerateHouseImagePath:
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        path = f"media/houses/{instance.id}/images"
        name = f"main.{ext}"
        return os.path.join(path, name)


house_path = GenerateHouseImagePath()


class House(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to=house_path, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_house",
    )
    points = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)
    not_completed_tasks_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
