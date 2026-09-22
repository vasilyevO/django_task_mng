from rest_framework import serializers
from django.utils import timezone

from apps.task.models import Task
from apps.task.serializers.tags import TagsSerializer
from apps.task.serializers.subtasks import SubTaskSerializer


class AllTasksSerializer(serializers.ModelSerializer):
    """Краткая информация о задаче (задача 12)."""

    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority']

class TaskCreateSerializer(serializers.ModelSerializer):
    """Создание задачи с проверкой корректности дедлайна (д/з 4)."""

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project',
            'status', 'priority', 'deadline', 'created_at',
        ]
        read_only_fields = ['id']

    def validate_deadline(self, value):
        is_update = self.instance is not None
        if is_update and value == self.instance.deadline:
            return value
        if value < timezone.now():
            raise serializers.ValidationError(
                'Deadline cannot be in the past.'
            )
        return value

class TaskInfoSerializer(serializers.ModelSerializer):
    """Подробная информация о задаче с вложенными тегами (задача 20)."""

    tags = TagsSerializer(many=True, read_only=True)  # вложенный сериализатор

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'status', 'priority',
            'tags', 'project', 'created_at', 'deadline',
        ]

class TaskDetailSerializer(serializers.ModelSerializer):
    """Подробная информация о задаче со всеми связанными подзадачами."""

    subtasks = SubTaskSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'project', 'tags', 'subtasks',
            'created_at', 'updated_at', 'deadline',
        ]

class TaskSerializer(serializers.ModelSerializer):
    """Полный сериализатор задачи для CRUD через Generic Views."""

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description',
            'status', 'deadline', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']