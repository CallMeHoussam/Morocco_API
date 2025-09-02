from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class City(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    region = models.CharField(max_length=120, blank=True, default="", db_index=True)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name = "City"
        verbose_name_plural = "Cities"
        constraints = [
            models.UniqueConstraint(fields=['name', 'region'], name='unique_city_region')
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-list') + f'?city_slug={self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    slug = models.SlugField(max_length=140, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")
    icon = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-list') + f'?category_slug={self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Event(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True, default="")
    location = models.CharField(max_length=200, blank=True, default="")
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="events")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events")
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(null=True, blank=True, db_index=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    image_url = models.URLField(blank=True, default="")
    ticket_url = models.URLField(blank=True, default="")

    class Meta:
        ordering = ["start_date"]
        indexes = [
            models.Index(fields=["city", "start_date"]),
            models.Index(fields=["category", "start_date"]),
            models.Index(fields=["is_active", "start_date"]),
            models.Index(fields=["start_date", "end_date"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lte=models.F('end_date')),
                name='end_date_after_start_date'
            )
        ]

    def __str__(self):
        return f"{self.title} — {self.city.name}"

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    @property
    def is_upcoming(self):
        return self.start_date >= timezone.now()

    @property
    def duration(self):
        if self.end_date:
            return self.end_date - self.start_date
        return None

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("end_date cannot be earlier than start_date.")
        if self.start_date and self.start_date < timezone.now() and not self.pk:
            raise ValidationError("Cannot create events in the past.")