from django.db.models import Count
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from django.utils import timezone
from django.shortcuts import get_object_or_404

from apps.task.models import Project, Tag, Task
from apps.core.models import Status
from apps.task.serializers.projects import AllProjectsSerializer
from apps.task.serializers.tags import TagsSerializer
from apps.task.serializers.tasks import (AllTasksSerializer,
                                         TaskInfoSerializer,
                                         CreateTaskSerializer,)


@api_view(['GET'])
def get_all_projects(request: Request) -> JsonResponse:
    """Список всех проектов (задача 11)."""
    projects = Project.objects.all()
    if not projects.exists():
        return JsonResponse([], status=status.HTTP_200_OK, safe=False)
    data = AllProjectsSerializer(projects, many=True).data
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def get_all_tasks(request: Request) -> JsonResponse:
    """Все задачи или задачи конкретного проекта (задача 13)."""
    project_name = request.query_params.get('project')
    if not project_name:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(project__name=project_name)

    if not tasks.exists():
        return JsonResponse([], status=status.HTTP_200_OK, safe=False)
    data = AllTasksSerializer(tasks, many=True).data
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def get_all_tags(request: Request) -> JsonResponse:
    """Список всех тегов."""
    tags = Tag.objects.all()
    if not tags.exists():
        return JsonResponse([], status=status.HTTP_200_OK, safe=False)
    data = TagsSerializer(tags, many=True).data
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def get_tag_by_id(request: Request, tag_id) -> JsonResponse:
    """Один тег по id."""
    tag = get_object_or_404(Tag, id=tag_id)
    data = TagsSerializer(tag).data
    return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_tag(request: Request, tag_id) -> JsonResponse:
    """Обновление тега."""
    tag = get_object_or_404(Tag, id=tag_id)
    serializer = TagsSerializer(tag, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_tag(request: Request) -> JsonResponse:
    """Создание тега."""
    serializer = TagsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_task(request: Request) -> JsonResponse:
    """Создание задачи (Задание 1 ДЗ)."""
    serializer = CreateTaskSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_task_statistics(request: Request) -> JsonResponse:
    """Статистика по задачам (Задание 3 ДЗ)."""
    total = Task.objects.count()
    by_status = Task.objects.values('status').annotate(count=Count('id'))
    overdue = Task.objects.filter(
        deadline__lt=timezone.now(),
    ).exclude(status=Status.DONE).count()

    statistics = {
        'total_tasks': total,
        'by_status': {row['status']: row['count'] for row in by_status},
        'overdue_tasks': overdue,
    }
    return JsonResponse(statistics, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_tag(request: Request, tag_id) -> JsonResponse:
    """Удаление тега (задание 19)."""
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    return JsonResponse(
        {'message': 'Tag deleted successfully'}, status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_task_by_id(request: Request, task_id) -> JsonResponse:
    """Детальная информация о задаче."""
    task = get_object_or_404(Task, id=task_id)
    data = TaskInfoSerializer(task).data
    return JsonResponse(data, status=status.HTTP_200_OK)
