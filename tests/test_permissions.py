from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from book.models import Book


def sample_book(
    name: str = "Book",
    author: str = "Author",
    daily_fee: Decimal = Decimal(10),
    cover: str = "HARD",
    inventory: int = 1,
) -> Book:
    pub_date = now()
    return Book.objects.create(
        name=name,
        author=author,
        daily_fee=daily_fee,
        cover=cover,
        inventory=inventory,
        pub_date=pub_date,
    )


class TestBookPermissions(APITestCase):

    def setUp(self):
        self.book = sample_book()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="userpassword",
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="adminpassword",
            is_staff=True,
            is_superuser=True,
        )
        self.list_url = reverse("book:book-list")
        self.detail_url = reverse("book:book-detail", kwargs={"pk": self.book.pk})

    def test_user_get_list(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_user_get_detail(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_post(self):
        payload = {
            "name": "Some",
            "author": "Author",
        }
        self.client.force_authenticate(user=self.user)
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 1)

    def test_user_patch(self):
        payload = {
            "name": "Some",
        }
        name = self.book.name
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(self.detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.book.refresh_from_db()
        self.assertEqual(self.book.name, name)

    def test_admin_post(self):
        payload = {
            "name": "Some",
            "author": "Author",
            "daily_fee": Decimal("10"),
            "cover": "HARD",
            "inventory": 1,
            "pub_date": now(),
        }
        self.client.force_authenticate(user=self.admin_user)
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_admin_patch(self):
        payload = {
            "name": "Some",
        }
        name = self.book.name
        self.client.force_authenticate(user=self.admin_user)
        res = self.client.patch(self.detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data["name"], name)
        self.book.refresh_from_db()
        self.assertEqual(res.data["name"], self.book.name)
