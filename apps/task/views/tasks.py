from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Status
from apps.task.models import Task
from apps.task.filters import TaskFilter
from apps.task.serializers.tasks import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """GET — список задач, POST"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE одной задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'


class TaskStatisticsView(APIView):
    """Статистика по задачам"""

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