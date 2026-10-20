from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits"
    )
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_habits",
    )
    periodicity = models.PositiveSmallIntegerField(default=1)  # дни
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveSmallIntegerField(
        verbose_name="Время на выполнение (сек)", help_text="Максимум 120 секунд"
    )  # секунды
    is_public = models.BooleanField(default=False)

    def clean(self):
        errors = {}

        # 1. reward и related_habit одновременно
        if self.reward and self.related_habit:
            errors["reward"] = (
                "Нельзя одновременно указать вознаграждение и связанную привычку."
            )

        # 2. duration <= 120
        if self.duration and self.duration > 120:
            errors["duration"] = "Время выполнения не должно превышать 120 секунд."

        # 3. related_habit должен быть приятной привычкой
        if self.related_habit and not self.related_habit.is_pleasant:
            errors["related_habit"] = (
                "Связанная привычка должна быть приятной (is_pleasant=True)."
            )

        # 4. приятная привычка не может иметь reward или related_habit
        if self.is_pleasant:
            if self.reward:
                errors["reward"] = "У приятной привычки не может быть вознаграждения."
            if self.related_habit:
                errors["related_habit"] = (
                    "У приятной привычки не может быть связанной привычки."
                )

        # 5. периодичность от 1 до 7
        if self.periodicity and not (1 <= self.periodicity <= 7):
            errors["periodicity"] = "Периодичность должна быть от 1 до 7 дней."

        if errors:
            raise ValidationError(errors)
