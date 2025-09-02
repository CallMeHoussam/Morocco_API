from django.contrib import admin
from django.utils.html import format_html
from .models import City, Category, Event

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "slug", "event_count")
    list_filter = ("region",)
    search_fields = ("name", "region", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("event_count",)
    
    def event_count(self, obj):
        return obj.events.count()
    event_count.short_description = "Events"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "event_count")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("event_count",)
    
    def event_count(self, obj):
        return obj.events.count()
    event_count.short_description = "Events"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "city", "category", "start_date", "end_date", "is_active", "created_by", "created_at")
    list_filter = ("city", "category", "start_date", "is_active", "created_at")
    search_fields = ("title", "description", "location")
    autocomplete_fields = ("city", "category", "created_by")
    readonly_fields = ("created_at", "updated_at", "is_upcoming")
    list_editable = ("is_active",)
    actions = ["activate_events", "deactivate_events"]
    
    fieldsets = (
        (None, {
            "fields": ("title", "short_description", "description")
        }),
        ("Location & Time", {
            "fields": ("city", "category", "location", "start_date", "end_date")
        }),
        ("Media & Links", {
            "fields": ("image_url", "ticket_url")
        }),
        ("Metadata", {
            "fields": ("created_by", "is_active", "created_at", "updated_at")
        })
    )
    
    def activate_events(self, request, queryset):
        queryset.update(is_active=True)
    activate_events.short_description = "Activate selected events"
    
    def deactivate_events(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_events.short_description = "Deactivate selected events"
    
    def is_upcoming(self, obj):
        return obj.is_upcoming
    is_upcoming.boolean = True
    is_upcoming.short_description = "Upcoming"