from rest_framework import viewsets, permissions, mixins
from rest_framework.viewsets import GenericViewSet

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    CreateBorrowingSerializer,
)


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        is_active = self.request.GET.get("is_active", None)
        user_id = self.request.GET.get("user_id", None)

        if user.is_staff:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user=user)

        if is_active and is_active.lower() in ("1", "true", "yes"):
            queryset = queryset.filter(actual_return_date__isnull=True)
        if user.is_staff and user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("user", "book")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action == "retrieve":
            return BorrowingDetailSerializer
        elif self.action == "create":
            return CreateBorrowingSerializer
        return BorrowingListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
