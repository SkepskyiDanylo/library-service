from celery import shared_task
from django.utils import timezone

from borrowing.models import Borrowing
from library_service.settings import telegram_bot


@shared_task
def check_borrowings():
    now = timezone.now()
    borrowings = Borrowing.objects.filter(
        expected_return_date__lte=now, actual_return_date__isnull=True
    )
    if borrowings.exists():
        for borrowing in borrowings.select_related("user", "book"):
            telegram_bot.expired_borrowing(borrowing)
    else:
        telegram_bot.no_expired_borrowings()
