from rest_framework import serializers

from apps.task.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Полная информация о категории — для чтения."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class CategoryTaskCountSerializer(serializers.ModelSerializer):
    """Категория вместе с количеством связанных задач."""

    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'tasks_count']


class CategoryCreateSerializer(serializers.ModelSerializer):
    """Создание и обновление категории (Д/З 2).

    Проверка уникальности имени вынесена в create/update
    по заданию.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def _ensure_name_is_unique(self, name: str) -> None:
        """Проверяет, что имя не занято другой категорией.

        Сравнение нормализуется в Python не зависим от диалекта БД.
        """
        normalized = name.strip().casefold()

        queryset = Category.objects.all()
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        clash = any(
            existing.strip().casefold() == normalized
            for existing in queryset.values_list('name', flat=True)
        )
        if clash:
            raise serializers.ValidationError(
                {'name': f'Category "{name}" already exists.'}
            )

    def create(self, validated_data: dict) -> Category:
        self._ensure_name_is_unique(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance: Category, validated_data: dict) -> Category:
        name = validated_data.get('name', instance.name)
        self._ensure_name_is_unique(name)
        return super().update(instance, validated_data)