from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Category, Event
from .serializers import CitySerializer, CategorySerializer, EventWriteSerializer, EventReadSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import EventFilter
from .pagination import StandardResultsSetPagination

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.annotate(event_count=Count('events'))
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "region", "slug"]
    ordering_fields = ["name", "region", "event_count"]
    pagination_class = StandardResultsSetPagination

class CityDetailView(generics.RetrieveAPIView):
    queryset = City.objects.annotate(event_count=Count('events'))
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.annotate(event_count=Count('events'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "event_count"]
    pagination_class = StandardResultsSetPagination

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.annotate(event_count=Count('events'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.select_related("city", "category", "created_by").filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ["title", "description", "short_description", "location"]
    ordering_fields = ["start_date", "created_at", "title"]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventWriteSerializer
        return EventReadSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filter by upcoming/past events
        timeframe = self.request.query_params.get("timeframe")
        if timeframe == "upcoming":
            qs = qs.filter(start_date__gte=timezone.now())
        elif timeframe == "past":
            qs = qs.filter(start_date__lt=timezone.now())
            
        # Filter by active status (admin only)
        if self.request.user.is_staff:
            show_inactive = self.request.query_params.get("show_inactive")
            if show_inactive == "true":
                qs = Event.objects.select_related("city", "category", "created_by")
                
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.select_related("city", "category", "created_by")
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'POST']:
            return EventWriteSerializer
        return EventReadSerializer

    def perform_destroy(self, instance):
        # Soft delete instead of actual deletion
        instance.is_active = False
        instance.save()

class UpcomingEventsView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ["title", "description", "short_description", "location"]
    ordering_fields = ["start_date", "created_at", "title"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Event.objects.select_related("city", "category", "created_by").filter(
            start_date__gte=timezone.now(),
            is_active=True
        )

@api_view(['GET'])
def event_stats(request):
    """Get statistics about events"""
    stats = {
        'total_events': Event.objects.filter(is_active=True).count(),
        'upcoming_events': Event.objects.filter(
            start_date__gte=timezone.now(),
            is_active=True
        ).count(),
        'cities_with_events': City.objects.filter(events__is_active=True).distinct().count(),
        'categories_with_events': Category.objects.filter(events__is_active=True).distinct().count(),
    }
    return Response(stats)