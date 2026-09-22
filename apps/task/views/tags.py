from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.permissions import IsAdminOrReadOnly
from apps.core.views import BaseDetailAPIView
from apps.task.models import Tag
from apps.task.serializers.tags import TagsSerializer


class TagListCreateView(generics.ListCreateAPIView):
    """Список тегов и создание нового."""

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAdminOrReadOnly]


class TagDetailView(BaseDetailAPIView):
    """Получение, обновление и удаление тега."""

    model = Tag
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, pk) -> Response:
        serializer = TagsSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        serializer = TagsSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk) -> Response:
        serializer = TagsSerializer(
            self.get_object(pk), data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk) -> Response:
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)