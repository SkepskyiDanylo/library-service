from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet

router = DefaultRouter()
router.register("", BookViewSet, basename="book")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "book"
