from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "pub_date",
            "cover",
            "inventory",
            "daily_fee",
        )