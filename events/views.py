from django.utils import timezone
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Category, Event
from .serializers import CitySerializer, CategorySerializer, EventSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "created_by_id", None) == getattr(request.user, "id", None)

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter,]
    search_fields = ["name", "region"]

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter,]
    search_fields = ["name"]

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.select_related("city", "category", "created_by").all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["city", "category"]  
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        upcoming = self.request.query_params.get("upcoming")
        if upcoming in ("1", "true", "True"):
            now = timezone.now()
            qs = qs.filter(start_date__gte=now)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.select_related("city", "category", "created_by").all()
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
class UpcomingEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["city", "category"]
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "created_at"]

    def get_queryset(self):
        now = timezone.now()
        return Event.objects.select_related("city", "category", "created_by").filter(start_date__gte=now)
