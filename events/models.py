from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone

class City(models.Model):
    name = models.CharField(max_length=120, unique=True)
    region = models.CharField(max_length=120, blank=True, default="")
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=['name', 'region'], name='unique_city_region')
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True, default="")
    location = models.CharField(max_length=200, blank=True, default="")
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="events")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, default="")
    ticket_url = models.URLField(blank=True, default="")
    external_source = models.CharField(max_length=50, blank=True, default="")
    external_id = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")