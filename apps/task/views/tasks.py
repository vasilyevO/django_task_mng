from django.db.models import Count
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Status
from apps.core.views import BaseDetailAPIView
from apps.task.models import Task
from apps.task.serializers.tasks import (
    AllTasksSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
)


class TaskListCreateView(APIView):
    """Список задач (с фильтром по проекту) и создание новой."""

    def get_queryset(self, request: Request):
        queryset = Task.objects.select_related('project')

        project_name = request.query_params.get('project')
        if project_name:
            queryset = queryset.filter(project__name=project_name)

        return queryset

    def get(self, request: Request) -> Response:
        serializer = AllTasksSerializer(self.get_queryset(request), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(BaseDetailAPIView):
    """Подробная информация о задаче, обновление и удаление."""

    queryset = Task.objects.prefetch_related('subtasks', 'tags')

    def get(self, request: Request, pk) -> Response:
        serializer = TaskDetailSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        serializer = TaskCreateSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk) -> Response:
        serializer = TaskCreateSerializer(
            self.get_object(pk), data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk) -> Response:
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskStatisticsView(APIView):
    """Статистика по задачам."""

    def get(self, request: Request) -> Response:
        by_status = Task.objects.values('status').annotate(count=Count('id'))
        overdue = Task.objects.filter(
            deadline__lt=timezone.now(),
        ).exclude(status=Status.DONE).count()

        statistics = {
            'total_tasks': Task.objects.count(),
            'by_status': {row['status']: row['count'] for row in by_status},
            'overdue_tasks': overdue,
        }
        return Response(statistics, status=status.HTTP_200_OK)