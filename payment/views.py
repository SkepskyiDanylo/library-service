from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext as _
from payment.models import Payment
from payment.serializers import PaymentDetailSerializer, PaymentListSerializer
from payment.stripe_sessions import check_session_paid, renew_session


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
        if self.action in ("retrieve", "renew"):
            return PaymentDetailSerializer
        return PaymentListSerializer

    @action(detail=True, methods=["post"], url_path="renew", url_name="renew")
    def renew(self, request, pk=None):
        instance = self.get_object()
        if instance.status != "EXPIRED":
            return Response(
                {"detail": _("Payment is not expired")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        renew_session(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SuccessPaymentView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        session = request.GET.get("session_id")
        session_status = check_session_paid(session)
        if session_status is True:
            payment = get_object_or_404(Payment, session_id=session)
            payment.status = "PAID"
            payment.save()
            return Response(
                {"detail": _("Payment was successful.")}, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_404_NOT_FOUND)


class CancelPaymentView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(
            {"detail": _("Payment was unsuccessful. You can pay later.")},
            status=status.HTTP_200_OK,
        )
