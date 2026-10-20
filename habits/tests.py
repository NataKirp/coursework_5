from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Habit


class HabitsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="secret123")
        self.client.force_authenticate(self.user)

    def test_create_habit(self):
        response = self.client.post(reverse("habit-list"), {
            "place": "дом", "time": "08:00", "action": "зарядка",
            "duration": 60, "periodicity": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duration_validation(self):
        response = self.client.post(reverse("habit-list"), {
            "place": "дом", "time": "08:00", "action": "зарядка",
            "duration": 200, "periodicity": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reward_and_related_conflict(self):
        pleasant = Habit.objects.create(
            user=self.user, place="x", time="10:00", action="y",
            is_pleasant=True, duration=60,
        )
        response = self.client.post(reverse("habit-list"), {
            "place": "дом", "time": "08:00", "action": "зарядка",
            "duration": 60, "periodicity": 1,
            "reward": "шоколад", "related_habit": pleasant.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_without_reward(self):
        response = self.client.post(reverse("habit-list"), {
            "place": "дом", "time": "08:00", "action": "ванна",
            "duration": 60, "is_pleasant": True, "reward": "конфета",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_edit_foreign_habit(self):
        other = User.objects.create_user(username="bob", password="secret123")
        habit = Habit.objects.create(
            user=other, place="x", time="10:00", action="y", duration=60,
        )
        response = self.client.patch(
            reverse("habit-detail", args=[habit.id]), {"action": "new"}
        )
        # Ожидаем 404, так как объект отфильтрован в get_queryset
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
