import django_filters
from django.utils import timezone
from .models import Event, City, Category

class EventFilter(django_filters.FilterSet):
    city = django_filters.ModelChoiceFilter(
        field_name="city", 
        queryset=City.objects.all(),
        to_field_name='id'
    )
    category = django_filters.ModelChoiceFilter(
        field_name="category", 
        queryset=Category.objects.all(),
        to_field_name='id'
    )
    
    city_slug = django_filters.CharFilter(field_name="city__slug", lookup_expr="iexact")
    category_slug = django_filters.CharFilter(field_name="category__slug", lookup_expr="iexact")
    
    date_from = django_filters.IsoDateTimeFilter(field_name="start_date", lookup_expr="gte")
    date_to = django_filters.IsoDateTimeFilter(field_name="start_date", lookup_expr="lte")
    
    # New filters
    region = django_filters.CharFilter(field_name="city__region", lookup_expr="iexact")
    upcoming = django_filters.BooleanFilter(method='filter_upcoming')
    created_by = django_filters.NumberFilter(field_name="created_by__id")
    
    class Meta:
        model = Event
        fields = [
            "city", "category", "city_slug", "category_slug", 
            "date_from", "date_to", "region", "upcoming", "created_by"
        ]
    
    def filter_upcoming(self, queryset, name, value):
        if value:
            return queryset.filter(start_date__gte=timezone.now())
        return queryset.filter(start_date__lt=timezone.now())