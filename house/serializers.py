from rest_framework import serializers

from .models import House


class HouseSerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        read_only=True, many=True, view_name="user-detail"
    )
    manager = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="user-detail"
    )
    tasklist = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="tasklist-detail", source="task_lists"
    )

    def create(self, validated_data):
        try:
            user = self.context["request"].user
            if user.house:
                raise serializers.ValidationError(
                    {
                        "error": "user is already a member of a house.Leave existing house to create a new one."
                    }
                )
            house = House.objects.create(**validated_data)
            house.manager = user
            user.house = house
            user.save()
            house.save()
            return house
        except Exception as e:
            raise serializers.ValidationError({"error": f"{e}"})

    class Meta:
        model = House
        fields = [
            "id",
            "url",
            "name",
            "image",
            "created_on",
            "description",
            "manager",
            "points",
            "completed_tasks_count",
            "not_completed_tasks_count",
            "members",
            "tasklist",
        ]
        read_only_fields = [
            "points",
            "completed_tasks_count",
            "not_completed_tasks_count",
        ]
