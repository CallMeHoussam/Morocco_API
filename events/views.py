from django.utils import timezone
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Category, Event
from .serializers import CitySerializer, CategorySerializer, EventSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import EventFilter

# Cities
class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "region", "slug"]
    ordering_fields = ["name", "region"]

# Categories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["name"]

# Events
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.select_related("city", "category", "created_by")
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "created_at", "title"]

    def get_queryset(self):
        qs = super().get_queryset()
        upcoming = self.request.query_params.get("upcoming")
        if upcoming in ("1", "true", "True"):
            qs = qs.filter(start_date__gte=timezone.now())
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.select_related("city", "category", "created_by")
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

class UpcomingEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "created_at", "title"]

    def get_queryset(self):
        return Event.objects.select_related("city", "category", "created_by").filter(
            start_date__gte=timezone.now()
        )
