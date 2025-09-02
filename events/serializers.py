from rest_framework import serializers
from django.utils import timezone
from .models import City, Category, Event
from django.conf import settings

class CitySerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ["id", "name", "region", "slug", "event_count"] 
        extra_kwargs = {
            'slug': {'read_only': True}
        }

    def get_event_count(self, obj):
        return obj.events.count()

class CategorySerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "icon", "event_count"] 
        extra_kwargs = {
            'slug': {'read_only': True}
        }

    def get_event_count(self, obj):
        return obj.events.count()

class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title", "description", "short_description", "location",
            "city", "category", "start_date", "end_date",
            "image_url", "ticket_url"
        ]

    def validate_start_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Start date must be in the future.")
        return value

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        
        if end and start and end < start:
            raise serializers.ValidationError({"end_date": "end_date cannot be earlier than start_date."})
        
        if end and (end - start).days > 30:
            raise serializers.ValidationError({"end_date": "Event cannot last more than 30 days."})
            
        return attrs

class EventReadSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    created_by_id = serializers.ReadOnlyField(source="created_by.id")
    city_detail = CitySerializer(source="city", read_only=True)
    category_detail = CategorySerializer(source="category", read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "title", "description", "short_description", "location",  
            "city", "city_detail", "category", "category_detail",
            "start_date", "end_date", "duration",
            "created_by", "created_by_id", "created_at", "updated_at",
            "is_upcoming", "is_active", "image_url", "ticket_url"
        ]
        extra_kwargs = {
            'city': {'write_only': True},
            'category': {'write_only': True}
        }