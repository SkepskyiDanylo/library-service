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
        if user.is_staff:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user=user)
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
