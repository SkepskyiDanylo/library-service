import stripe

from library_service import settings
from payment.models import Payment

stripe.api_key = settings.STRIPE_API_KEY


def calculate_payment_price(borrowing):
    delta = (borrowing.expected_return_date - borrowing.borrow_date).days
    price = borrowing.book.daily_fee * delta
    return price


def create_checkout_session(borrowing) -> str:
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
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )
    return Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=price,
    )
