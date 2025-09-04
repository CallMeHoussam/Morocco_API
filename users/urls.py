from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserDetailView,
    UserProfileUpdateView,
    PasswordChangeView,
    user_stats,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", UserDetailView.as_view(), name="user-detail"),
    path("me/profile/", UserProfileUpdateView.as_view(), name="user-profile-update"),
    path("me/password/", PasswordChangeView.as_view(), name="password-change"),
    path("me/stats/", user_stats, name="user-stats"),
]