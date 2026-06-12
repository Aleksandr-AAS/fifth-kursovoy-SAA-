from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from habits.models import Habit
from datetime import time

User = get_user_model()


class HabitAPITest(TestCase):
    """Тесты для API привычек"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com", password="userpass123"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="otherpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit_authenticated(self):
        """Авторизованный пользователь может создать привычку"""
        url = reverse("habit-list")
        data = {
            "action": "Прогулка",
            "tiny_action": "Надеть обувь",
            "estimated_time": 60,
            "place": "Парк",
            "time": "18:00:00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().user, self.user)

    def test_create_habit_unauthenticated(self):
        """Неавторизованный пользователь не может создать привычку"""
        self.client.force_authenticate(user=None)
        url = reverse("habit-list")
        data = {
            "action": "Тест",
            "tiny_action": "Начать",
            "estimated_time": 60,
            "time": "18:00:00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_with_invalid_time(self):
        """Нельзя создать привычку с временем выполнения > 120 секунд"""
        url = reverse("habit-list")
        data = {
            "action": "Слишком долго",
            "tiny_action": "Начать",
            "estimated_time": 130,
            "time": "18:00:00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user_habits(self):
        """Пользователь видит только свои привычки"""
        Habit.objects.create(
            user=self.user,
            action="Моя привычка",
            tiny_action="Начать",
            estimated_time=60,
            time=time(10, 0),
        )
        Habit.objects.create(
            user=self.other_user,
            action="Чужая привычка",
            tiny_action="Начать",
            estimated_time=60,
            time=time(11, 0),
        )
        url = reverse("habit-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Моя привычка")

    def test_update_own_habit(self):
        """Пользователь может обновить свою привычку"""
        habit = Habit.objects.create(
            user=self.user,
            action="Старое действие",
            tiny_action="Начать",
            estimated_time=60,
            time=time(10, 0),
        )
        url = reverse("habit-detail", args=[habit.id])
        response = self.client.patch(url, {"action": "Новое действие"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "Новое действие")

    def test_delete_own_habit(self):
        """Пользователь может удалить свою привычку"""
        habit = Habit.objects.create(
            user=self.user,
            action="Удалить меня",
            tiny_action="Начать",
            estimated_time=60,
            time=time(10, 0),
        )
        url = reverse("habit-detail", args=[habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_cannot_update_other_habit(self):
        """Пользователь не может обновить чужую привычку"""
        habit = Habit.objects.create(
            user=self.other_user,
            action="Чужая привычка",
            tiny_action="Начать",
            estimated_time=60,
            time=time(10, 0),
        )
        url = reverse("habit-detail", args=[habit.id])
        response = self.client.patch(url, {"action": "Попытка взлома"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habits_list(self):
        """Публичные привычки видны без авторизации"""
        Habit.objects.create(
            user=self.user,
            action="Публичная привычка",
            tiny_action="Начать",
            estimated_time=60,
            time=time(10, 0),
            is_public=True,
        )
        Habit.objects.create(
            user=self.user,
            action="Приватная привычка",
            tiny_action="Начать",
            estimated_time=60,
            time=time(11, 0),
            is_public=False,
        )
        self.client.force_authenticate(user=None)
        url = reverse("public-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Публичная привычка")
