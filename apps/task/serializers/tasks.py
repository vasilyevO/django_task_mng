from rest_framework import serializers

from apps.task.models import Task
from apps.task.serializers.tags import TagsSerializer


class AllTasksSerializer(serializers.ModelSerializer):
    """Краткая информация о задаче (задача 12)."""

    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority']

class CreateTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для создания задачи (Задание 1)."""

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']
        read_only_fields = ['id']

class TaskInfoSerializer(serializers.ModelSerializer):
    """Подробная информация о задаче с вложенными тегами (задача 20)."""

    tags = TagsSerializer(many=True, read_only=True)  # вложенный сериализатор

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'status', 'priority',
            'tags', 'project', 'created_at', 'deadline',
        ]