from datetime import timedelta

from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APITestCase
from rest_framework import status

from borrowing.models import Borrowing
from book.models import Book
from user.models import User


class BorrowingEndpointTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="pass123")
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            name="Test Book", author="Author", inventory=3, daily_fee=10, pub_date=now()
        )
        self.url = reverse("borrowing:borrowing-list")

    def test_successful_borrowing(self):
        payload = {
            "book": self.book.id,
            "expected_return_date": (now().date() + timedelta(days=5)).isoformat(),
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)

        borrowing = Borrowing.objects.first()
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 2)

    def test_fail_if_book_inventory_zero(self):
        self.book.inventory = 0
        self.book.save()

        payload = {
            "book": self.book.id,
            "expected_return_date": (now().date() + timedelta(days=5)).isoformat(),
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Book inventory must be greater than 0.", str(response.data))

    def test_fail_if_expected_return_date_in_past(self):
        payload = {
            "book": self.book.id,
            "expected_return_date": (now().date() - timedelta(days=1)).isoformat(),
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Expected return date must be after borrowing date.", str(response.data)
        )


class BorrowingReturnBookTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="pass123")
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            name="Return Test Book",
            author="Author",
            inventory=1,
            daily_fee=10,
            pub_date=now(),
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=now().date(),
            expected_return_date=now().date() + timedelta(days=3),
        )
        self.url = reverse(
            "borrowing:borrowing-return", kwargs={"pk": self.borrowing.id}
        )

    def test_successful_return(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()
        self.borrowing.refresh_from_db()

        self.assertEqual(self.book.inventory, 2)
        self.assertIsNotNone(self.borrowing.actual_return_date)

    def test_fail_if_already_returned(self):
        self.client.post(self.url)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The book is already returned.", str(response.data))
