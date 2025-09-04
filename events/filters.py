import django_filters
from django.utils import timezone
from .models import Event

class EventFilter(django_filters.FilterSet):
    city = django_filters.NumberFilter(field_name="city__id")
    category = django_filters.NumberFilter(field_name="category__id")
    city_slug = django_filters.CharFilter(field_name="city__slug")
    category_slug = django_filters.CharFilter(field_name="category__slug")
    date_from = django_filters.DateTimeFilter(field_name="start_date", lookup_expr="gte")
    date_to = django_filters.DateTimeFilter(field_name="start_date", lookup_expr="lte")
    region = django_filters.CharFilter(field_name="city__region")

    class Meta:
        model = Event
        fields = ["city", "category", "city_slug", "category_slug", "date_from", "date_to", "region"]