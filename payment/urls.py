from django.urls import path, include
from rest_framework import routers

from payment.views import PaymentViewSet, SuccessPaymentView, CancelPaymentView

router = routers.DefaultRouter()
router.register("", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("session/success/", SuccessPaymentView.as_view(), name="success"),
    path("session/cancel/", CancelPaymentView.as_view(), name="cancel"),
]

app_name = "payment"
