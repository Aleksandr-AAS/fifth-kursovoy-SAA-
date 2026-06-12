
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Habit
from .serializers import HabitSerializer, HabitPublicSerializer


class HabitPagination(PageNumberPagination):
    """Пагинация для привычек"""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками:
    - Пользователь видит/редактирует только свои привычки
    - При создании привычки автоматически подставляется текущий пользователь
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Пользователь видит только свои привычки"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании автоматически привязываем текущего пользователя"""
        serializer.save(user=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра публичных привычек (доступно всем, только чтение)
    """

    serializer_class = HabitPublicSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Только публичные привычки"""
        return Habit.objects.filter(is_public=True)
