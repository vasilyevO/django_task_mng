# --- apps/task/serializers/tags.py (задача 14) ---
from rest_framework import serializers

from apps.task.models import Tag


class TagsSerializer(serializers.ModelSerializer):
    """Полная информация о теге."""

    class Meta:
        model = Tag
        fields = '__all__'