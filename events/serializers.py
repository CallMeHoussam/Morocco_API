from rest_framework import serializers
from .models import City, Category, Event

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "region"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    city_detail = CitySerializer(source="city", read_only=True)
    category_detail = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "title", "description",
            "city", "city_detail",
            "category", "category_detail",
            "start_date", "end_date",
            "created_by", "created_at",
        ]

    def validate(self, attrs):
        start = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        end = attrs.get("end_date") or getattr(self.instance, "end_date", None)
        if end and start and end < start:
            raise serializers.ValidationError("end_date cannot be earlier than start_date.")
        return attrs
