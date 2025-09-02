from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import UserProfile

CustomUser = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        
        self.user = CustomUser.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="testpass123"
        )

    def test_user_registration(self):
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login(self):
        url = reverse('user-login')
        data = {
            "username": "existinguser",
            "password": "testpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_password_change(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('password-change')
        data = {
            "old_password": "testpass123",
            "new_password": "newpass123",
            "new_password_confirm": "newpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="testmodel",
            email="model@example.com",
            password="testpass123"
        )
        self.assertEqual(user.username, "testmodel")
        self.assertTrue(user.check_password("testpass123"))
        
        # Test that profile was created
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, UserProfile)