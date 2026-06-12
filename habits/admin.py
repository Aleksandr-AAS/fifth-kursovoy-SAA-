from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "tiny_action",
        "time",
        "is_public",
        "is_pleasant",
    )
    list_filter = ("is_public", "is_pleasant", "periodicity")
    search_fields = ("action", "user__email")
    readonly_fields = ("created_at", "updated_at")
