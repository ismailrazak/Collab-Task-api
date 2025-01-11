from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True)
    new_password = serializers.CharField(write_only=True, required=False)
    house = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="house-detail"
    )

    def validate(self, data):
        request = self.context.get("request")
        if request.method == "POST":
            if not data.get("password", None):
                raise serializers.ValidationError({"info": "Please enter a password."})

        if request.method == "PUT" or request.method == "PATCH":
            if data.get("new_password") and not data.get("password"):
                raise serializers.ValidationError(
                    {
                        "info": "Please enter your old password alongside your new password."
                    }
                )
            if data.get("password") and not data.get("new_password"):
                raise serializers.ValidationError(
                    {"info": "Please enter your new password too."}
                )
        return data

    def create(self, validated_data):
        if validated_data.get("new_password"):
            new_password = validated_data.pop("new_password")
        if validated_data.get("password"):
            password = validated_data.pop("password")
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("new_password"):
            if check_password(validated_data.get("password"), instance.password):
                instance.set_password(validated_data.get("new_password"))
                instance.save()
            else:
                raise serializers.ValidationError(
                    "Password does not match existing password."
                )
            return instance
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = [
            "id",
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "new_password",
            "image",
            "house",
        ]
