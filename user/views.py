from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from user.serializers import UserSerializer


@extend_schema(tags=["User"])
class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = get_user_model().objects.none()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
