from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from apps.task.models import SubTask
from apps.task.filters import SubTaskFilter
from apps.task.serializers.subtasks import SubTaskSerializer


class SubTaskListCreateView(generics.ListCreateAPIView):
    """GET — список подзадач, POST"""

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = SubTaskFilter

    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SubTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE одной подзадачи"""

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'subgitask_id'