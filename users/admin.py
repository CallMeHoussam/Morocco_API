from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_verified")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_verified")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-created_at",)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "notifications_enabled", "language", "timezone")
    list_filter = ("notifications_enabled", "language")
    search_fields = ("user__username", "user__email")