import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Устанавливает webhook для Telegram бота"

    def handle(self, *args, **options):
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
        webhook_url = settings.TELEGRAM_WEBHOOK_URL  # нужно добавить в .env
        if not webhook_url:
            self.stdout.write(self.style.ERROR("TELEGRAM_WEBHOOK_URL не задан"))
            return

        response = requests.post(url, json={"url": webhook_url})
        self.stdout.write(self.style.SUCCESS(f"Webhook установлен: {response.json()}"))
