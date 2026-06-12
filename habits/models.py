from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Habit(models.Model):
    """
    Модель привычки
    """

    class DaysOfWeek(models.TextChoices):
        MONDAY = "mon", "Понедельник"
        TUESDAY = "tue", "Вторник"
        WEDNESDAY = "wed", "Среда"
        THURSDAY = "thu", "Четверг"
        FRIDAY = "fri", "Пятница"
        SATURDAY = "sat", "Суббота"
        SUNDAY = "sun", "Воскресенье"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="пользователь",
    )

    # Основное действие
    action = models.CharField(max_length=255, verbose_name="действие")

    # Двухминутная версия (для старта)
    tiny_action = models.CharField(
        max_length=255,
        verbose_name="двухминутное действие",
        help_text="То, с чего начинается привычка (не более 2 минут)",
    )

    # Время выполнения (секунды, не более 120)
    estimated_time = models.PositiveIntegerField(
        default=120,
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name="время выполнения (секунды)",
        help_text="Не более 120 секунд (2 минуты)",
    )

    # Место выполнения
    place = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="место"
    )

    # Время начала (для напоминаний)
    time = models.TimeField(verbose_name="время напоминания")

    # Дни недели (JSON поле)
    days_of_week = models.JSONField(default=list, blank=True, verbose_name="дни недели")

    # Вознаграждение (опционально)
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="вознаграждение"
    )

    # Приятная привычка (ссылка на другую привычку)
    pleasant_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="related_to",
        verbose_name="приятная привычка",
    )

    # Флаг: является ли привычка приятной
    is_pleasant = models.BooleanField(default=False, verbose_name="приятная привычка")

    # Периодичность (раз в сколько дней)
    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="периодичность (дни)",
    )

    # Видимость в публичном списке
    is_public = models.BooleanField(default=False, verbose_name="публичная")

    # Telegram chat ID (для отправки уведомлений)
    telegram_chat_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Telegram chat ID"
    )

    # Даты создания и обновления
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"
        ordering = ["time"]

    def __str__(self):
        return f"{self.user.email} — {self.action}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
