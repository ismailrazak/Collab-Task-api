from django.shortcuts import render
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import COMPLETED, NOT_COMPLETED, Attachment, Task, TaskList
from .permissions import (
    IsAllowedToEditAttachmentOrNone,
    IsAllowedToEditTaskOrNone,
    IsTaskListCreatorOrNone,
)
from .serializers import AttachmentSerializer, TaskListSerializer, TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related(
        "created_by", "completed_by", "tasklist"
    ).prefetch_related("attachments")
    # queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAllowedToEditTaskOrNone,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("status",)

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            updated_queryset = queryset.filter(created_by=self.request.user)
            return updated_queryset
        except Exception as e:
            return None

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        status = self.request.data.get("status")
        if status == COMPLETED:
            serializer.save(completed_by=self.request.user, completed_on=timezone.now())
        elif status == NOT_COMPLETED:
            task = self.get_object()
            if task.status == COMPLETED:
                serializer.save(completed_by=None, completed_on=None)
        serializer.save()


class TaskListViewSet(
    GenericViewSet,
    UpdateModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
):

    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [
        IsTaskListCreatorOrNone,
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AttachmentViewSet(
    GenericViewSet,
    UpdateModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (IsAllowedToEditAttachmentOrNone,)
