from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        
        self.user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="testpass123"
        )

    def test_user_registration(self):
        response = self.client.post('/api/v1/users/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)

    def test_user_login(self):
        data = {
            "username": "existinguser",
            "password": "testpass123"
        }
        response = self.client.post('/api/v1/users/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testmodel",
            email="model@example.com",
            password="testpass123"
        )
        self.assertEqual(user.username, "testmodel")
        self.assertTrue(user.check_password("testpass123"))