from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.timezone import now
from django.utils.translation.trans_null import gettext_lazy as _
from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from payment.models import Payment


class BorrowingListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.full_name", read_only=True)
    book = serializers.CharField(source="book.name", read_only=True)
    book_id = serializers.CharField(source="book.id", read_only=True)
    user_id = serializers.CharField(source="user.id", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "book_id",
            "user",
            "user_id",
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("id", "money_to_pay", "session_id", "session_url", "status", "type")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )


class CreateBorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ("id", "user", "actual_return_date", "borrow_date")

    def validate_book(self, value):
        if value.inventory < 1:
            raise serializers.ValidationError(
                _("Book inventory must be greater than 0.")
            )
        return value

    def validate(self, validated_data):
        expected_return_date = validated_data.get("expected_return_date")
        if expected_return_date < now().date():
            raise serializers.ValidationError(
                _("Expected return date must be after borrowing date.")
            )
        return validated_data

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.get("book")
            book.inventory = book.inventory - 1
            book.save()
            borrowing = Borrowing.objects.create(**validated_data)
        return borrowing
