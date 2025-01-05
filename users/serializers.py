from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
    username = serializers.CharField(read_only=True)
    new_password = serializers.CharField(write_only=True,required=False)

    def create(self, validated_data):

        if validated_data.get('password'):
            password = validated_data.pop('password')
            print(password)
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('new_password'):
            if check_password(validated_data.get('password'),instance.password):
                instance.set_password(validated_data.get('new_password'))
                instance.save()
            else:
                raise serializers.ValidationError('Password does not match existing password.')
        return instance

#todo : check password update fucntionality

    class Meta:
        model =User
        fields = ['id','username','first_name','last_name','email','password','new_password']
        # extra_kwargs = {
        #     "url": {"view_name": "users-detail"},
        # }


