from rest_framework import serializers
from .models import User

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
            if instance.password == validated_data.get('password'):
                instance.set_password(validated_data.get('new_password'))
                return instance



    class Meta:
        model =User
        fields = ['id','username','first_name','last_name','email','password','new_password']
        # extra_kwargs = {
        #     "url": {"view_name": "users-detail"},
        # }


