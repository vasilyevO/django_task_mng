from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.views import BaseDetailAPIView
from apps.task.models import SubTask
from apps.task.serializers.subtasks import SubTaskCreateSerializer


class SubTaskListCreateView(APIView):
    """Список подзадач и создание новой (д/з 5)."""

    def get_queryset(self, request: Request):
        """Возвращает подзадачи, при наличии фильтра — только нужной задачи."""
        queryset = SubTask.objects.select_related('task')

        task_id = request.query_params.get('task')
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset

    def get(self, request: Request) -> Response:
        subtasks = self.get_queryset(request)
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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