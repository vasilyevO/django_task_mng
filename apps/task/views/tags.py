from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.views import BaseDetailAPIView
from apps.task.models import Tag
from apps.task.serializers.tags import TagsSerializer


class TagListCreateView(APIView):
    """Список тегов и создание нового."""

    def get(self, request: Request) -> Response:
        serializer = TagsSerializer(Tag.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = TagsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagDetailView(BaseDetailAPIView):
    """Получение, обновление и удаление тега."""

    model = Tag

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