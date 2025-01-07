from rest_framework.viewsets import ModelViewSet
from .serializers import HouseSerializer
from .models import House
from .permissions import IsHouseManagerOrNone
from rest_framework.decorators import action, permission_classes
from rest_framework.views import Response
from rest_framework import status
from django.contrib.auth import get_user_model
class HouseViewSet(ModelViewSet):
    models = House
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = IsHouseManagerOrNone,

    @action(detail=True,methods=['post','get'],permission_classes=[])
    def join(self,request,pk):
        try:
            user =request.user
            house = self.get_object()
            if house.members.filter(id=user.id).exists():
                return Response({'info':'user is already a member of the house.'},status=status.HTTP_400_BAD_REQUEST)

            if request.user.house:
                return Response({'info':'user is already a member of another house.'},status=status.HTTP_400_BAD_REQUEST)

            user.house = house
            user.save()
            return Response({'info':'user has been added to the house successfully.'},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':f'{e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True,methods=['post','get'],permission_classes=[])
    def leave(self,request,pk):
        try:
            user =request.user
            house = self.get_object()
            if house.members.filter(id=request.user.id).exists():
                user.house = None
                user.save()
                return Response({'info':'user has left the house successfully.'},status=status.HTTP_200_OK)
            else:
                return Response({'info':'user is not a member of the house.'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':f'{e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post', 'get'],permission_classes = [IsHouseManagerOrNone,])
    def remove(self,request,pk):
        try:
            house = self.get_object()
            user_id = request.data.get('user')
            user = get_user_model().objects.get(id = user_id)
            if user.house != None and user.house !=house:
                return Response({'info':'user is a member of another house.'},status=status.HTTP_400_BAD_REQUEST)

            if house.members.filter(id=user_id).exists():
                user.house = None
                user.save()
                return Response({'info':'user has been removed successfully.'},status=status.HTTP_200_OK)
            else:
                return Response({'info':'user does not exist.'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'info':f'{e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

