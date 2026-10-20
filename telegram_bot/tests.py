from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from habits.models import Habit
from users.models import User

from .tasks import send_habit_reminders


class RemindersTests(TestCase):
    @patch("telegram_bot.tasks.send_message")
    def test_send_reminders(self, mock_send):
        now = timezone.localtime()
        user = User.objects.create_user(
            username="john", password="x", chat_id="111",
        )
        Habit.objects.create(
            user=user, place="дом", time=now.time().replace(second=0, microsecond=0),
            action="зарядка", duration=60,
        )
        send_habit_reminders()
        self.assertEqual(mock_send.call_count, 1)

