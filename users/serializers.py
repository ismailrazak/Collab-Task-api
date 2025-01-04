from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
    username = serializers.CharField(read_only=True)

    def create(self, validated_data):
        if validated_data.get('password'):
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
        user = User.objects.create(**validated_data)
        user.save()
        return user

    class Meta:
        model =User
        fields = ['id','url','username','first_name','last_name','email','password']

