from django.core.exceptions import ValidationError


def validate_two_minute_rule(value):
    """Проверка, что привычка занимает не более 2 минут"""
    if value > 120:
        raise ValidationError(
            "Привычка должна занимать не более 2 минут (120 секунд) согласно правилу двух минут."
        )


def validate_not_reward_and_pleasant_habit(data):
    """Валидация: привычка не может иметь и вознаграждение, и приятную привычку"""
    reward = data.get("reward")
    pleasant_habit = data.get("pleasant_habit")
    if reward and pleasant_habit:
        raise ValidationError(
            "Нельзя указывать одновременно вознаграждение и связанную приятную привычку."
        )


def validate_pleasant_habit_own_fields(data):
    """Валидация: приятная привычка не может иметь вознаграждение или другую приятную привычку"""
    if data.get("is_pleasant"):
        if data.get("reward"):
            raise ValidationError("Приятная привычка не может иметь вознаграждение.")
        if data.get("pleasant_habit"):
            raise ValidationError(
                "Приятная привычка не может быть связана с другой привычкой."
            )


def validate_periodicity(value):
    """Проверка периодичности (от 1 до 7 дней)"""
    if value < 1 or value > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")
