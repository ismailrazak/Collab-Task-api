from idlelib.rpc import request_queue

from rest_framework import serializers

from house.models import House

from .models import Attachment, Task, TaskList


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, many=False
    )
    tasklist = serializers.HyperlinkedRelatedField(
        view_name="tasklist-detail", queryset=TaskList.objects.all(), many=False
    )
    completed_by = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, many=False
    )
    attachments = serializers.HyperlinkedRelatedField(
        many=True, view_name="attachment-detail", read_only=True
    )

    def validate_tasklist(self, value):
        request = self.context.get("request")
        if value.house != request.user.house:
            raise serializers.ValidationError(
                {"error": "house selected is not your own house."}
            )
        return value

    class Meta:
        model = Task
        fields = [
            "id",
            "url",
            "created_on",
            "completed_on",
            "completed_by",
            "created_by",
            "description",
            "status",
            "name",
            "tasklist",
            "attachments",
        ]
        read_only_fields = ["created_on", "completed_on", "created_by", "completed_by"]


class TaskListSerializer(serializers.ModelSerializer):
    house = serializers.HyperlinkedRelatedField(
        view_name="house-detail", queryset=House.objects.all(), many=False
    )
    created_by = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, many=False
    )
    tasks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="task-detail"
    )

    class Meta:
        model = TaskList
        fields = [
            "id",
            "url",
            "house",
            "created_by",
            "status",
            "name",
            "created_on",
            "completed_on",
            "tasks",
        ]
        read_only_fields = ["status", "created_on"]


class AttachmentSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(
        view_name="task-detail", queryset=Task.objects.all(), many=False
    )

    def validate_task(self, value):
        request = self.context.get("request")
        if value.tasklist.house != request.user.house:
            raise serializers.ValidationError(
                {"error": "task selected is not from your house."}
            )
        return value

    class Meta:
        model = Attachment
        fields = ["id", "url", "created_on", "data", "task"]
