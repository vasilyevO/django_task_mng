from rest_framework import serializers

from apps.task.models import Project


class AllProjectsSerializer(serializers.ModelSerializer):
    """Краткая информация о проекте."""

    class Meta:
        model = Project
        fields = ['id', 'name', 'created_at']

class CreateProjectSerializer(serializers.ModelSerializer):
    """Создание и обновление проекта."""

    description = serializers.CharField(required=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_description(self, value: str) -> str:
        min_length = 30
        if len(value.strip()) < min_length:
            raise serializers.ValidationError(
                f'Description must be at least {min_length} characters long.'
            )
        return value


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Подробная информация о проекте с количеством файлов."""

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'count_of_files']


