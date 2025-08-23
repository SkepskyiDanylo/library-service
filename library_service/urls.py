from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularYAMLAPIView,
    SpectacularJSONAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from library_service import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/books/", include("book.urls", namespace="book")),
    path("api/users/", include("user.urls", namespace="user")),
    path("api/borrowings/", include("borrowing.urls", namespace="borrowing")),
    path("api/payments/", include("payment.urls", namespace="payment")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("yml/", SpectacularYAMLAPIView.as_view(), name="yml-schema")]
    urlpatterns += [path("json/", SpectacularJSONAPIView.as_view(), name="schema")]
    urlpatterns += [
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        )
    ]
    urlpatterns += [path("redoc/", SpectacularRedocView.as_view(), name="redoc")]
