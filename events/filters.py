import django_filters
from .models import Event, City, Category

class EventFilter(django_filters.FilterSet):
    # allow filtering by IDs…
    city = django_filters.ModelChoiceFilter(field_name="city", queryset=City.objects.all())
    category = django_filters.ModelChoiceFilter(field_name="category", queryset=Category.objects.all())

    # …or by slugs
    city_slug = django_filters.CharFilter(field_name="city__slug", lookup_expr="iexact")
    category_slug = django_filters.CharFilter(field_name="category__slug", lookup_expr="iexact")

    # date range filtering
    date_from = django_filters.IsoDateTimeFilter(field_name="start_date", lookup_expr="gte")
    date_to = django_filters.IsoDateTimeFilter(field_name="start_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ["city", "category", "city_slug", "category_slug", "date_from", "date_to"]
