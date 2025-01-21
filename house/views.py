from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action, permission_classes
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from .models import House
from .permissions import IsHouseManagerOrNone
from .serializers import HouseSerializer


class HouseViewSet(ModelViewSet):
    models = House
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = (IsHouseManagerOrNone,)
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ("name",)
    ordering_fields = ("completed_tasks_count",)
    filterset_fields = ("members",)

    @action(detail=True, methods=["post", "get"], permission_classes=[])
    def join(self, request, pk):
        try:
            user = request.user
            house = self.get_object()
            if house.members.filter(id=user.id).exists():
                return Response(
                    {"info": "user is already a member of the house."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if request.user.house:
                return Response(
                    {"info": "user is already a member of another house."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.house = house
            user.save()
            return Response(
                {"info": "user has been added to the house successfully."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"error while joining."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post", "get"], permission_classes=[])
    def leave(self, request, pk):
        try:
            user = request.user
            house = self.get_object()
            if house.members.filter(id=request.user.id).exists():
                user.house = None
                managed_house = House.objects.filter(manager=user)
                if managed_house:
                    managed_house.delete()
                user.save()
                return Response(
                    {"info": "user has left the house successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"info": "user is not a member of the house."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": f"error while leaving."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=True,
        methods=["post", "get"],
        permission_classes=[
            IsHouseManagerOrNone,
        ],
    )
    def remove(self, request, pk):
        try:
            house = self.get_object()
            user_id = request.data.get("user")
            user = get_user_model().objects.get(id=user_id)
            if user.house != None and user.house != house:
                return Response(
                    {"info": "user is a member of another house."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if house.members.filter(id=user_id).exists():
                user.house = None
                user.save()
                return Response(
                    {"info": "user has been removed successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"info": "user does not belong to this house."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"info": f"error while removing."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
