"""
URL configuration for Morroco_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from events.views import home
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "events": request.build_absolute_uri('/api/events/'),
        "users": request.build_absolute_uri('/api/users/'),
        "token": request.build_absolute_uri('/api/token/'),
        "token_refresh": request.build_absolute_uri('/api/token/refresh/'),
    })
urlpatterns = [
    path('', home, name='home'),
    path('', lambda request: redirect('/api/events/')),
    path('admin/', admin.site.urls),
    path('api/events/', include('events.urls')),
    path('api/users/', include('users.urls')),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/token/', include('rest_framework_simplejwt.urls')),
]
