from django.contrib import admin
from .models import City, Category, Event

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region")
    search_fields = ("name", "region")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "city", "category", "start_date", "created_by", "created_at")
    list_filter = ("city", "category", "start_date")
    search_fields = ("title", "description")
