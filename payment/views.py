from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.serializers import PaymentDetailSerializer, PaymentListSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Payment.objects.all()
        else:
            queryset = Payment.objects.filter(borrowing__user=user)
        queryset = queryset.select_related("borrowing", "borrowing__user")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentListSerializer
