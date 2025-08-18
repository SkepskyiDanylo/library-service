from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/book-service/", include("book.urls", namespace="book")),
]
