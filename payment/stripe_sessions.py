import stripe
from rest_framework.reverse import reverse

from library_service import settings
from payment.models import Payment

stripe.api_key = settings.STRIPE_API_KEY


def calculate_payment_price(borrowing):
    delta = (borrowing.expected_return_date - borrowing.borrow_date).days
    price = borrowing.book.daily_fee * delta
    return price


def create_checkout_session(request, borrowing) -> str:
    success_url = (
        request.build_absolute_uri(reverse("payment:success"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = request.build_absolute_uri(reverse("payment:cancel"))

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


def check_session_paid(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        return True
    return False
