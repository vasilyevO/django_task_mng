from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Status
from apps.core.pagination import StandardPagination
from apps.core.views import BaseDetailAPIView, PaginatedListMixin
from apps.task.models import SubTask
from apps.task.serializers.subtasks import SubTaskCreateSerializer


class SubTaskListCreateView(PaginatedListMixin, APIView):
    """Список подзадач с фильтрами и пагинацией, создание новой."""

    pagination_class = StandardPagination

    def get_queryset(self, request: Request):
        queryset = SubTask.objects.select_related('task')

        task_id = request.query_params.get('task')
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        task_title = request.query_params.get('task_title')
        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)

        subtask_status = request.query_params.get('status')
        if subtask_status:
            queryset = queryset.filter(status=self._validate_status(subtask_status))

        return queryset

    @staticmethod
    def _validate_status(value: str) -> str:
        """Проверяет, что статус входит в допустимые значения."""
        normalized = value.strip().lower()
        allowed = {choice.value for choice in Status}

        if normalized not in allowed:
            raise ValidationError({
                'status': (
                    f'Unknown status: "{value}". '
                    f'Allowed values: {", ".join(sorted(allowed))}.'
                ),
            })

        return normalized

    def get(self, request: Request) -> Response:
        return self.list_response(
            self.get_queryset(request),
            SubTaskCreateSerializer,
        )

    def post(self, request: Request) -> Response:
        serializer = SubTaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SubTaskDetailUpdateDeleteView(BaseDetailAPIView):
    """Получение, обновление и удаление подзадачи (д/з 5)."""

    model = SubTask

    def get(self, request: Request, pk) -> Response:
        serializer = SubTaskCreateSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        serializer = SubTaskCreateSerializer(
            self.get_object(pk),
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk) -> Response:
        serializer = SubTaskCreateSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk) -> Response:
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)