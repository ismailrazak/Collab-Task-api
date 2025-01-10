from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Task, TaskList, Attachment, NOT_COMPLETED
from rest_framework.mixins import UpdateModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from .serializers import TaskSerializer,TaskListSerializer,AttachmentSerializer
from .permissions import IsTaskListCreatorOrNone,IsAllowedToEditAttachmentOrNone,IsAllowedToEditTaskOrNone
from .models import COMPLETED
from django.utils import timezone

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = IsAllowedToEditTaskOrNone,

    def get_queryset(self):
        queryset = super().get_queryset()
        updated_queryset = queryset.filter(created_by=self.request.user)
        return updated_queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        status = self.request.data.get('status')
        if status ==COMPLETED:
            serializer.save(completed_by=self.request.user,completed_on=timezone.now())
        elif status==NOT_COMPLETED:
            task = self.get_object()
            if task.status==COMPLETED:
                serializer.save(completed_by=None,completed_on=None)
class TaskListViewSet(GenericViewSet,UpdateModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin):

    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsTaskListCreatorOrNone,]

class AttachmentViewSet(GenericViewSet,UpdateModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = IsAllowedToEditAttachmentOrNone,