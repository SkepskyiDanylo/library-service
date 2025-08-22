from celery import shared_task

from library_service.settings import telegram_bot
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


@shared_task
def send_payment(payment_id):
    payment = Payment.objects.get(id=payment_id)
    telegram_bot.success_payment(payment)
