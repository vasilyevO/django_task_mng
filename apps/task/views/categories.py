from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.task.models import Category
from apps.task.serializers.categories import (
    CategoryCreateSerializer,
    CategorySerializer,
    CategoryTaskCountSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD по категориям. Удаление — мягкое (is_deleted/deleted_at)."""

    queryset = Category.objects.all()  # менеджер уже скрывает «удалённые»
    serializer_class = CategorySerializer

    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return CategoryCreateSerializer
        if self.action == 'count_tasks':
            return CategoryTaskCountSerializer
        return CategorySerializer

    @action(detail=False, methods=['get'], url_path='count-tasks')
    def count_tasks(self, request: Request) -> Response:
        """Количество задач в каждой категории."""
        queryset = self.filter_queryset(
            self.get_queryset().annotate(tasks_count=Count('tasks')),
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
