from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "telegram_chat_id", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "telegram_chat_id")
    readonly_fields = ("date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Telegram", {"fields": ("telegram_chat_id",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
