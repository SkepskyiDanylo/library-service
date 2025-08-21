from django.db import transaction
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext as _
from rest_framework import permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

import borrowing
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    CreateBorrowingSerializer,
)
from library_service.settings import telegram_bot
from payment.stripe_sessions import create_checkout_session, create_fine_session


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

        if self.action == "list":
            queryset = queryset.select_related("user", "book")
        elif self.action == "retrieve":
            queryset = queryset.select_related("user", "book").prefetch_related(
                "payments"
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action in ("retrieve", "return_book"):
            return BorrowingDetailSerializer
        elif self.action == "create":
            return CreateBorrowingSerializer
        return BorrowingListSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user, borrow_date=now().date())
        telegram_bot.new_borrowing(borrowing)
        create_checkout_session(self.request, borrowing)

    @action(detail=True, methods=["post"], url_name="return", url_path="return")
    def return_book(self, request, pk=None):
        instance = self.get_object()

        if instance.actual_return_date:
            return Response(
                {"detail": _("The book is already returned.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book = instance.book
        with transaction.atomic():
            book.inventory = book.inventory + 1
            book.save()
            instance.actual_return_date = now().date()
            instance.save()
            if now().date() > instance.expected_return_date:
                overdue = (instance.expected_return_date - now().date()).days
                create_fine_session(request, instance, book, overdue)
                instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
