from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from habits.models import Habit
from datetime import time

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели привычки"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_create_valid_habit(self):
        """Создание валидной привычки"""
        habit = Habit.objects.create(
            user=self.user,
            action="Читать книги",
            tiny_action="Прочитать 1 страницу",
            estimated_time=60,
            place="Дома",
            time=time(19, 0),
            reward="Конфета",
            is_public=True,
        )
        self.assertEqual(habit.action, "Читать книги")
        self.assertEqual(habit.estimated_time, 60)
        self.assertEqual(habit.user.email, "test@example.com")
        self.assertTrue(habit.is_public)

    def test_estimated_time_validation(self):
        """Время выполнения не более 120 секунд (правило двух минут)"""
        habit = Habit(
            user=self.user,
            action="Слишком долго",
            tiny_action="Начать",
            estimated_time=130,
            time=time(19, 0),
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_validation(self):
        """Периодичность от 1 до 7 дней"""
        habit = Habit(
            user=self.user,
            action="Слишком частая привычка",
            tiny_action="Начать",
            estimated_time=60,
            time=time(19, 0),
            periodicity=8,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_str_method(self):
        """Проверка строкового представления"""
        habit = Habit.objects.create(
            user=self.user,
            action="Медитация",
            tiny_action="Сесть на коврик",
            estimated_time=120,
            time=time(8, 0),
        )
        self.assertEqual(str(habit), "test@example.com — Медитация")
