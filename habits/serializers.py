from rest_framework import serializers
from .models import Habit
from .validators import (
    validate_not_reward_and_pleasant_habit,
    validate_pleasant_habit_own_fields,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычки"""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def validate(self, data):
        # Проверка: нельзя указывать одновременно вознаграждение и приятную привычку
        validate_not_reward_and_pleasant_habit(data)

        # Проверка: приятная привычка не может иметь вознаграждение или другую приятную привычку
        validate_pleasant_habit_own_fields(data)

        # Проверка: время выполнения не более 120 секунд (дубль, на всякий случай)
        if data.get("estimated_time", 0) > 120:
            raise serializers.ValidationError(
                "Привычка должна занимать не более 2 минут (120 секунд)"
            )

        return data


class HabitPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек (только чтение)"""

    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Habit
        fields = ("id", "action", "place", "time", "user_email", "is_pleasant")
        read_only_fields = (
            "id",
            "action",
            "place",
            "time",
            "user_email",
            "is_pleasant",
        )
