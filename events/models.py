from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    region = models.CharField(max_length=120, blank=True, default="", db_index=True)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="events")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events")
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(null=True, blank=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["start_date"]
        indexes = [
            models.Index(fields=["city", "start_date"]),
            models.Index(fields=["category", "start_date"]),
        ]

    def __str__(self):
        return f"{self.title} — {self.city.name}"

    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.start_date >= timezone.now()

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("end_date cannot be earlier than start_date.")
