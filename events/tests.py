from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import City, Category, Event

class EventAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        self.city = City.objects.create(
            name="Marrakech",
            region="Marrakech-Safi",
            slug="marrakech"
        )
        
        self.category = Category.objects.create(
            name="Music Festival",
            slug="music-festival"
        )
        
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            city=self.city,
            category=self.category,
            start_date=timezone.now() + timezone.timedelta(days=7),
            created_by=self.user
        )
    
    def test_create_event(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('event-list-create')
        data = {
            "title": "New Event",
            "description": "New Event Description",
            "city": self.city.id,
            "category": self.category.id,
            "start_date": (timezone.now() + timezone.timedelta(days=14)).isoformat(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
    
    def test_list_events(self):
        url = reverse('event-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
class ModelTests(TestCase):
    def test_city_str(self):
        city = City.objects.create(name="Casablanca", slug="casablanca")
        self.assertEqual(str(city), "Casablanca")
    
    def test_event_validation(self):
        event = Event(
            title="Test Event",
            description="Test",
            city=City.objects.create(name="Test", slug="test"),
            category=Category.objects.create(name="Test", slug="test"),
            start_date=timezone.now() - timezone.timedelta(days=1), 
            created_by=User.objects.create_user("test")
        )
        with self.assertRaises(ValidationError):
            event.full_clean()