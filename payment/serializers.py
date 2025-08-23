from rest_framework import serializers

from borrowing.serializers import BorrowingListSerializer
from payment.models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    user_fullname = serializers.CharField(
        source="borrowing.user.full_name", read_only=True
    )
    user_id = serializers.CharField(source="borrowing.user.id", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "money_to_pay",
            "type",
            "status",
            "borrowing",
            "user_fullname",
            "user_id",
            "session_url",
            "session_id",
        )


class PaymentDetailSerializer(serializers.ModelSerializer):
    borrowing = BorrowingListSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "money_to_pay",
            "type",
            "status",
            "borrowing",
            "session_url",
            "session_id",
        )


class ResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
