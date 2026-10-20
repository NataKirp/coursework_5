from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UsersTests(APITestCase):
    def test_register(self):
        url = reverse("register")
        data = {"username": "john", "password": "secret123", "chat_id": "123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="john").exists())

    def test_token(self):
        User.objects.create_user(username="john", password="secret123")
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "john", "password": "secret123"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

