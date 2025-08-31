from django.contrib import admin
from .models import City, Category, Event

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "slug")
    list_filter = ("region",)
    search_fields = ("name", "region", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "city", "category", "start_date", "end_date", "created_by", "created_at")
    list_filter = ("city", "category", "start_date")
    search_fields = ("title", "description")
    autocomplete_fields = ("city", "category", "created_by")
