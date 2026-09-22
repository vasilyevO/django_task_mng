from rest_framework import serializers

from apps.task.models import SubTask

class SubTaskSerializer(serializers.ModelSerializer):
    """Полный сериализатор подзадачи для CRUD."""

    class Meta:
        model = SubTask
        fields = [
            'id', 'title', 'description', 'task',
            'status', 'deadline', 'owner', 'created_at',
        ]
        read_only_fields = ['id', 'owner', 'created_at']

class SubTaskCreateSerializer(serializers.ModelSerializer):
    """Создание и обновление подзадачи"""

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            'id', 'title', 'description', 'task',
            'status', 'deadline', 'created_at',
        ]
        read_only_fields = ['id']

