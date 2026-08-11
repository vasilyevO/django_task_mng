# apps/core/lagacy.py

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response



class PaginatedListMixin:
    """Подключает пагинацию к обычному APIView.

    Наследники задают `pagination_class`. Если он не задан —
    список отдаётся целиком, без разбиения на страницы.
    """

    pagination_class = None
    _paginator = None

    @property
    def paginator(self):
        """Ленивая инициализация пагинатора (один на запрос)."""
        if self._paginator is None and self.pagination_class is not None:
            self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset, self.request, view=self,
        )

    def get_paginated_response(self, data) -> Response:
        return self.paginator.get_paginated_response(data)

    def list_response(self, queryset, serializer_class) -> Response:
        """Собирает ответ со страницей или полным списком."""
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

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