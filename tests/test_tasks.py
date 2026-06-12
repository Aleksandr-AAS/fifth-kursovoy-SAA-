from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from habits.models import Habit
from telegram_bot.tasks import send_habit_reminders, send_telegram_message

User = get_user_model()


class CeleryTasksTest(TestCase):
    """Тесты для Celery-задач"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            telegram_chat_id="123456789",
        )

    def test_send_telegram_message_mock(self):
        """Отправка сообщения (мок, без интернета)"""
        result = send_telegram_message("123456789", "Тестовое сообщение")
        self.assertIn("mock", result)
        self.assertTrue(result["mock"])

    def test_send_habit_reminders_no_habits(self):
        """Нет привычек — нет уведомлений"""
        result = send_habit_reminders()
        self.assertEqual(result, "Sent 0 reminders")

    def test_send_habit_reminders_with_habit(self):
        """Привычка с прошедшим временем отправляет уведомление"""
        past_time = (timezone.now() - timezone.timedelta(minutes=5)).time()
        Habit.objects.create(
            user=self.user,
            action="Тестовая привычка",
            tiny_action="Начать тест",
            estimated_time=60,
            time=past_time,
        )
        result = send_habit_reminders()
        self.assertEqual(result, "Sent 1 reminders")
