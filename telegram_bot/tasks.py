from celery import shared_task
from django.utils import timezone

from habits.models import Habit

from .services import send_message


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    habits = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute,
    ).exclude(user__chat_id__isnull=True).exclude(user__chat_id="")

    for habit in habits:
        text = (
            f"Напоминание: {habit.action} в {habit.place} "
            f"({habit.time.strftime('%H:%M')})"
        )
        send_message(habit.user.chat_id, text)
