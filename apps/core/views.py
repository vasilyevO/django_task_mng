# apps/core/lagacy.py

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView


class BaseDetailAPIView(APIView):
    """Базовый класс для detail-View: инкапсулирует получение объекта по pk.

    Наследники задают либо `model`, либо `queryset`

    """

    model = None
    queryset = None

    def get_queryset(self):
        if self.queryset is not None:
            return self.queryset.all()
        return self.model._default_manager.all()

    def get_object(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)