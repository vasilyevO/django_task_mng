from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Category, SubTask, Task


class SubTaskInline(admin.TabularInline):
    """Подзадачи прямо в карточке задачи."""

    model = SubTask
    extra = 0
    fields = ('title', 'status', 'deadline')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category_list', 'deadline', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    inlines = (SubTaskInline,)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Task]:
        """Задачи вместе с категориями — без N+1 в списке."""
        return super().get_queryset(request).prefetch_related('categories')

    @admin.display(description='Categories')
    def category_list(self, obj: Task) -> str:
        """Категории задачи одной строкой."""
        return ', '.join(category.name for category in obj.categories.all())


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')

    def get_queryset(self, request: HttpRequest) -> QuerySet[SubTask]:
        """Подзадачи вместе с родительской задачей — без N+1."""
        return super().get_queryset(request).select_related('task')