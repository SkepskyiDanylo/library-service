import stripe
from rest_framework.reverse import reverse

from library_service import settings
from payment.models import Payment

FINE_MULTIPLIER = 2
stripe.api_key = settings.STRIPE_API_KEY


def calculate_payment_price(borrowing):
    delta = (borrowing.expected_return_date - borrowing.borrow_date).days
    price = borrowing.book.daily_fee * delta
    return price


def get_return_urls(request):
    success_url = (
        request.build_absolute_uri(reverse("payment:success"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = request.build_absolute_uri(reverse("payment:cancel"))
    return success_url, cancel_url


def create_checkout_session(request, borrowing):
    if not settings.STRIPE_API_KEY:
        return
    success_url, cancel_url = get_return_urls(request)

    price = calculate_payment_price(borrowing)
    book = borrowing.book
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Borrowing for book {book.name}",
                    },
                    "unit_amount": int(price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=price,
    )


def create_fine_session(request, borrowing, book, overdue):
    if not settings.STRIPE_API_KEY:
        return
    success_url, cancel_url = get_return_urls(request)
    price = book.daily_fee * FINE_MULTIPLIER * abs(overdue)
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Overdue fine for book {borrowing.book.name}",
                    },
                    "unit_amount": int(price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=price,
        type="FINE",
    )


def check_session_paid(session_id):
    if not settings.STRIPE_API_KEY:
        return
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        return True
    return False


def get_sessions_for_payment(payment):
    if not settings.STRIPE_API_KEY:
        return
    session_id = payment.session_id
    sessions = stripe.checkout.Session.retrieve(session_id)
    return sessions


def renew_session(request, payment):
    if not settings.STRIPE_API_KEY:
        return
    price = payment.money_to_pay
    borrowing = payment.borrowing
    success_url, cancel_url = get_return_urls(request)
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Borrowing for book {borrowing.book.name}",
                    },
                    "unit_amount": int(price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    payment.session_url = session.url
    payment.session_id = session.id
    payment.status = "PENDING"
    payment.save()
    return payment
