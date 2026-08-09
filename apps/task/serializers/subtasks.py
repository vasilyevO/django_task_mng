from rest_framework import serializers

from apps.task.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    """Краткая информация о подзадаче — для вложения в задачу."""

    class Meta:
        model = SubTask
        fields = [
            'id', 'title', 'description',
            'status', 'deadline', 'created_at',
        ]


class SubTaskCreateSerializer(serializers.ModelSerializer):
    """Создание и обновление подзадачи (Задание 1)."""

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            'id', 'title', 'description', 'task',
            'status', 'deadline', 'created_at',
        ]
        read_only_fields = ['id']