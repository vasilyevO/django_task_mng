from django.db.models import Count
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.task.models import Project, Tag, Task

from apps.task.serializers.projects import AllProjectsSerializer


@api_view(['GET'])
def get_all_projects(request: Request) -> JsonResponse:
    """Список всех проектов (задача 11)."""
    projects = Project.objects.all()
    if not projects.exists():
        return JsonResponse([], status=status.HTTP_200_OK, safe=False)
    data = AllProjectsSerializer(projects, many=True).data
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

