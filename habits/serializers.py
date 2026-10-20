from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
        )
        read_only_fields = ("user",)

    def validate(self, attrs):
        instance = Habit(**attrs)
        if self.instance:
            for field, value in attrs.items():
                setattr(self.instance, field, value)
            instance = self.instance
        instance.clean()
        return attrs
