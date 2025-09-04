from django.utils import timezone
from django.db.models import Count
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Category, Event
from .serializers import CitySerializer, CategorySerializer, EventWriteSerializer, EventReadSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import EventFilter
from .pagination import StandardResultsSetPagination
from .services import event_api_service

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.annotate(event_count=Count('events'))
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "region"]
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
    search_fields = ["name"]
    ordering_fields = ["name", "event_count"]
    pagination_class = StandardResultsSetPagination

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.annotate(event_count=Count('events'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class EventListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventWriteSerializer
        return EventReadSerializer

    def get_queryset(self):
        qs = Event.objects.select_related("city", "category", "created_by").filter(
            is_active=True, is_approved=True
        )
        
        timeframe = self.request.query_params.get("timeframe", "")
        
        if timeframe == "upcoming":
            qs = qs.filter(start_date__gte=timezone.now())
        elif timeframe == "past":
            qs = qs.filter(start_date__lt=timezone.now())
        elif timeframe == "new":
            one_week_ago = timezone.now() - timezone.timedelta(days=7)
            qs = qs.filter(created_at__gte=one_week_ago)
        elif timeframe == "today":
            today = timezone.now().date()
            qs = qs.filter(start_date__date=today)
        elif timeframe == "this_week":
            today = timezone.now().date()
            end_of_week = today + timezone.timedelta(days=6)
            qs = qs.filter(start_date__date__range=[today, end_of_week])
        elif timeframe == "this_month":
            today = timezone.now().date()
            first_day = today.replace(day=1)
            next_month = first_day.replace(month=first_day.month % 12 + 1, year=first_day.year + (first_day.month // 12))
            last_day = next_month - timezone.timedelta(days=1)
            qs = qs.filter(start_date__date__range=[first_day, last_day])
        
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.select_related("city", "category", "created_by")
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return EventWriteSerializer
        return EventReadSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class UpcomingEventsView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Event.objects.select_related("city", "category", "created_by").filter(
            start_date__gte=timezone.now(), is_active=True, is_approved=True
        )

@api_view(['GET'])
def event_stats(request):
    stats = {
        'total_events': Event.objects.filter(is_active=True).count(),
        'upcoming_events': Event.objects.filter(start_date__gte=timezone.now(), is_active=True).count(),
        'cities_with_events': City.objects.filter(events__is_active=True).distinct().count(),
        'categories_with_events': Category.objects.filter(events__is_active=True).distinct().count(),
    }
    return Response(stats)

class NewEventsView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        one_week_ago = timezone.now() - timezone.timedelta(days=7)
        return Event.objects.select_related("city", "category", "created_by").filter(
            created_at__gte=one_week_ago, is_active=True, is_approved=True
        ).order_by('-created_at')

class TodayEventsView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        today = timezone.now().date()
        return Event.objects.select_related("city", "category", "created_by").filter(
            start_date__date=today, is_active=True, is_approved=True
        ).order_by('start_date')

class ThisWeekEventsView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        today = timezone.now().date()
        end_of_week = today + timezone.timedelta(days=6)
        return Event.objects.select_related("city", "category", "created_by").filter(
            start_date__date__range=[today, end_of_week], is_active=True, is_approved=True
        ).order_by('start_date')

class ThisMonthEventsView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        today = timezone.now().date()
        first_day = today.replace(day=1)
        next_month = first_day.replace(month=first_day.month % 12 + 1, year=first_day.year + (first_day.month // 12))
        last_day = next_month - timezone.timedelta(days=1)
        return Event.objects.select_related("city", "category", "created_by").filter(
            start_date__date__range=[first_day, last_day], is_active=True, is_approved=True
        ).order_by('start_date')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def external_events(request):
    source = request.GET.get('source', 'eventbrite')
    events = event_api_service.search_eventbrite_events() if source == 'eventbrite' else event_api_service.search_ticketmaster_events()
    return Response({'source': source, 'count': len(events), 'events': events})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def import_external_event(request):
    from .models import Event, City, Category
    from datetime import datetime
    
    external_event = request.data
    required_fields = ['title', 'start_date', 'source', 'external_id']
    
    for field in required_fields:
        if field not in external_event:
            return Response({'error': f'Missing field: {field}'}, status=400)
    
    if Event.objects.filter(external_source=external_event['source'], external_id=external_event['external_id']).exists():
        return Response({'error': 'Event already imported'}, status=400)
    
    city, _ = City.objects.get_or_create(
        name=external_event.get('venue', {}).get('city', 'Unknown'),
        defaults={'region': 'Unknown', 'slug': 'unknown'}
    )
    
    category, _ = Category.objects.get_or_create(
        name=external_event.get('category', 'General'),
        defaults={'slug': 'general'}
    )
    
    try:
        start_date = datetime.fromisoformat(external_event['start_date'].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(external_event['end_date'].replace('Z', '+00:00')) if external_event.get('end_date') else None
    except (ValueError, TypeError):
        return Response({'error': 'Invalid date format'}, status=400)
    
    event = Event.objects.create(
        title=external_event['title'],
        description=external_event.get('description', ''),
        city=city,
        category=category,
        start_date=start_date,
        end_date=end_date,
        location=external_event.get('venue', {}).get('address', ''),
        image_url=external_event.get('image_url', ''),
        ticket_url=external_event.get('url', ''),
        external_source=external_event['source'],
        external_id=external_event['external_id'],
        created_by=request.user,
        is_active=True,
        is_approved=True
    )
    
    serializer = EventReadSerializer(event)
    return Response({'message': 'Event imported', 'event': serializer.data}, status=201)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def approve_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.is_approved = True
        event.save()
        return Response({"message": "Event approved"})
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def pending_events(request):
    events = Event.objects.filter(is_approved=False, is_active=True)
    serializer = EventReadSerializer(events, many=True)
    return Response(serializer.data)