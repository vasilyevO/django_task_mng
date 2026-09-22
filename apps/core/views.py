from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class BaseDetailAPIView(APIView):
    """Базовый класс для detail-эндпоинтов: получает объект или 404."""

    model = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)