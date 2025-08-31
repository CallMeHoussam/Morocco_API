import os
import sys
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "events": request.build_absolute_uri("/api/events/"),
        "events_upcoming": request.build_absolute_uri("/api/events/upcoming/"),
        "cities": request.build_absolute_uri("/api/events/cities/"),
        "categories": request.build_absolute_uri("/api/events/categories/"),
        "users_register": request.build_absolute_uri("/api/users/register/"),
        "token_obtain": request.build_absolute_uri("/api/token/"),
        "token_refresh": request.build_absolute_uri("/api/token/refresh/"),
        "docs_swagger": request.build_absolute_uri("/swagger/"),
        "docs_redoc": request.build_absolute_uri("/redoc/"),
        "health": request.build_absolute_uri("/health/"),
    })

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})

schema_view = get_schema_view(
    openapi.Info(
        title="Morocco API",
        default_version="v1",
        description="Events in Moroccan cities with categories & JWT auth",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", api_root, name="api-root"),
    path("health/", health, name="health"),
    path("admin/", admin.site.urls),

    path("api/events/", include("events.urls")),
    path("api/users/", include("users.urls")),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
