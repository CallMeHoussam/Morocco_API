from django.contrib import admin
from .models import City, Category, Event

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "slug", "event_count")
    list_filter = ("region",)
    search_fields = ("name", "region")
    prepopulated_fields = {"slug": ("name",)}

    def event_count(self, obj):
        return obj.events.count()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "event_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def event_count(self, obj):
        return obj.events.count()

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "category", "start_date", "is_active", "is_approved")
    list_filter = ("city", "category", "is_active", "is_approved")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("is_active", "is_approved")