from rest_framework.serializers import ModelSerializer

from apps.task.models import Project


class AllProjectsSerializer(ModelSerializer):
    """Краткая информация о проекте."""

    class Meta:
        model = Project
        fields = ['id', 'name']


