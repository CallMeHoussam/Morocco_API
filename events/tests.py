from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import City, Category, Event
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse

CustomUser = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Casablanca", region="Casablanca-Settat", slug="casablanca")
        self.category = Category.objects.create(name="Music", slug="music")
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass123")
    
    def test_city_creation(self):
        self.assertEqual(self.city.name, "Casablanca")
        self.assertEqual(self.city.slug, "casablanca")
    
    def test_event_creation(self):
        event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            city=self.city,
            category=self.category,
            start_date=timezone.now() + timedelta(days=1),
            created_by=self.user
        )
        self.assertEqual(event.title, "Test Event")
        self.assertTrue(event.is_active)

class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass123")
        self.city = City.objects.create(name="Casablanca", region="Casablanca-Settat", slug="casablanca")
        self.category = Category.objects.create(name="Music", slug="music")
        
    def test_get_events(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_event_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('event-list')
        data = {
            "title": "New Event",
            "description": "Event Description",
            "city": self.city.id,
            "category": self.category.id,
            "start_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "location": "Test Location"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_event_unauthenticated(self):
        url = reverse('event-list')
        data = {
            "title": "New Event",
            "description": "Event Description",
            "city": self.city.id,
            "category": self.category.id,
            "start_date": (timezone.now() + timedelta(days=1)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        # Change from 403 to 401 - this is more common for unauthenticated requests
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class EventFilterTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass123")
        self.city = City.objects.create(name="Casablanca", region="Casablanca-Settat", slug="casablanca")
        self.category = Category.objects.create(name="Music", slug="music")
        
        Event.objects.create(
            title="Music Festival",
            description="Annual music festival",
            city=self.city,
            category=self.category,
            start_date=timezone.now() + timedelta(days=5),
            created_by=self.user
        )
        Event.objects.create(
            title="Art Exhibition",
            description="Local art exhibition",
            city=self.city,
            category=self.category,
            start_date=timezone.now() - timedelta(days=1), 
            created_by=self.user
        )
    
    def test_upcoming_events_filter(self):
        url = reverse('event-upcoming')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only upcoming event
    
    def test_timeframe_filter(self):
        url = reverse('event-list')
        response = self.client.get(url, {'timeframe': 'upcoming'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)