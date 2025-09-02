import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.db import connection
from django.db.utils import OperationalError
from django.utils import timezone

@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "v1": {
            "events": request.build_absolute_uri("/api/v1/events/"),
            "events_upcoming": request.build_absolute_uri("/api/v1/events/upcoming/"),
            "cities": request.build_absolute_uri("/api/v1/events/cities/"),
            "categories": request.build_absolute_uri("/api/v1/events/categories/"),
            "users_register": request.build_absolute_uri("/api/v1/users/register/"),
            "token_obtain": request.build_absolute_uri("/api/v1/token/"),
            "token_refresh": request.build_absolute_uri("/api/v1/token/refresh/"),
            "token_verify": request.build_absolute_uri("/api/v1/token/verify/"),
        },
        "docs_swagger": request.build_absolute_uri("/swagger/"),
        "docs_redoc": request.build_absolute_uri("/redoc/"),
        "health": request.build_absolute_uri("/health/"),
        "admin": request.build_absolute_uri("/admin/"),
    })

@api_view(["GET"])
def health(request):
    """Comprehensive health check endpoint"""
    status_info = {
        "status": "ok", 
        "timestamp": timezone.now().isoformat(),
        "service": "Morocco API"
    }
    
    # Database health check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            status_info["database"] = "healthy"
    except OperationalError as e:
        status_info["database"] = "unhealthy"
        status_info["database_error"] = str(e)
        status_info["status"] = "degraded"
    
    # Cache health check (if Redis is configured)
    try:
        from django.core.cache import cache
        cache.set('health_check', 'ok', 5)
        if cache.get('health_check') == 'ok':
            status_info["cache"] = "healthy"
        else:
            status_info["cache"] = "unhealthy"
            status_info["status"] = "degraded"
    except Exception as e:
        status_info["cache"] = "not_configured"
    
    return Response(status_info, status=200 if status_info["status"] == "ok" else 503)

schema_view = get_schema_view(
    openapi.Info(
        title="Morocco API",
        default_version="v1",
        description="Events in Moroccan cities with categories & JWT auth",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", api_root, name="api-root"),
    path("health/", health, name="health"),
    path("admin/", admin.site.urls),

    # API v1 endpoints
    path("api/v1/", include([
        path("", api_root, name="api-root-v1"),
        path("events/", include("events.urls")),
        path("users/", include("users.urls")),
        path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    ])),
    
    # Backward compatibility with old endpoints
    path("api/", include([
        path("", api_root, name="api-root-legacy"),
        path("events/", include("events.urls")),
        path("users/", include("users.urls")),
    ])),

    # Documentation
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    
    # Debug toolbar (development only)
]

# Add debug toolbar in development
if os.getenv('DJANGO_ENVIRONMENT', 'development') == 'development':
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass