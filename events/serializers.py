from rest_framework import serializers
from django.utils import timezone
from .models import City, Category, Event

class CitySerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ["id", "name", "region", "slug", "event_count"]

    def get_event_count(self, obj):
        return obj.events.count()

class CategorySerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "event_count"]

    def get_event_count(self, obj):
        return obj.events.count()

class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["title", "description", "short_description", "location",
                 "city", "category", "start_date", "end_date", "image_url", "ticket_url"]

    def validate_start_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Start date must be in the future.")
        return value

class EventReadSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    city_detail = CitySerializer(source="city", read_only=True)
    category_detail = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "short_description", "location",
                 "city", "city_detail", "category", "category_detail", "start_date",
                 "end_date", "created_by", "created_at", "updated_at", "is_active",
                 "image_url", "ticket_url"]