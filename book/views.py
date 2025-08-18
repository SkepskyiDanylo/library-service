from rest_framework import viewsets

from book.models import Book
from book.permissions import BookPermission
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (BookPermission,)