from celery import shared_task

from payment.models import Payment
from payment.stripe_sessions import get_sessions_for_payment


@shared_task
def check_expired_sessions():
    payments = Payment.objects.filter(status="PENDING")
    for payment in payments:
        session = get_sessions_for_payment(payment)
        if session.status == "expired":
            payment.status = "EXPIRED"
            payment.save()
