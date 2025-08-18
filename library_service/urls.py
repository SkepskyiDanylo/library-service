from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/books/", include("book.urls", namespace="book")),
    path("api/users/", include("user.urls", namespace="user")),
    path("api/borrowings/", include("borrowing.urls", namespace="borrowing")),
]
