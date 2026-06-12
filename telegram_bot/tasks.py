import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from habits.models import Habit
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_message(chat_id, message):
    """Отправка сообщения через Telegram бота"""
    if (
        not settings.TELEGRAM_BOT_TOKEN
        or settings.TELEGRAM_BOT_TOKEN == "placeholder_token"
    ):
        logger.info(f"[MOCK] Telegram message to {chat_id}: {message}")
        return {"mock": True, "chat_id": chat_id, "message": message}

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Telegram error: {e}")
        return {"error": str(e)}


@shared_task
def send_habit_reminders():
    """
    Периодическая задача: отправляет напоминания о привычках,
    у которых наступило время выполнения.
    """
    now = timezone.now().time()
    today = timezone.now().strftime("%a").lower()  # mon, tue, wed, etc.

    habits = Habit.objects.filter(
        time__lte=now,  # время уже наступило или прошло
        # is_active=True,
        user__telegram_chat_id__isnull=False,
    )

    # Фильтрация по дням недели (если заданы)
    habits = [h for h in habits if not h.days_of_week or today in h.days_of_week]

    count = 0
    for habit in habits:
        message = (
            f"🔔 Напоминание о привычке!\n\n"
            f"🎯 Действие: {habit.tiny_action}\n"
            f"📍 Место: {habit.place or 'любое'}\n"
            f"⏱️ Время выполнения: {habit.estimated_time} сек\n"
            f"✨ Награда: {habit.reward or 'без награды'}"
        )
        send_telegram_message.delay(habit.user.telegram_chat_id, message)
        count += 1

    logger.info(f"Отправлено {count} напоминаний о привычках")
    return f"Sent {count} reminders"
