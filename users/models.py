from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default="")
    location = models.CharField(max_length=100, blank=True, default="")
    website = models.URLField(blank=True, default="")
    is_verified = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    email_notifications = models.BooleanField(default=True)
    newsletter_subscription = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username} - {self.email}"

    def clean(self):
        if not self.email:
            raise ValidationError("Email is required")
        if self.date_of_birth:
            min_age_date = timezone.now().date() - timezone.timedelta(days=13*365)
            if self.date_of_birth > min_age_date:
                raise ValidationError("User must be at least 13 years old")

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    notifications_enabled = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default="en")
    timezone = models.CharField(max_length=50, default="UTC")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile of {self.user.username}"