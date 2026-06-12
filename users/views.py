
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(APIView):
    """Получение профиля текущего пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
