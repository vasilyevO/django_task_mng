from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Category, Project, SubTask, Tag, Task
from apps.core.models import Status


class SubTaskInline(admin.TabularInline):
    """Подзадачи прямо в карточке задачи."""

    model = SubTask
    extra = 0
    fields = ('title', 'status', 'deadline')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'short_title', 'status', 'priority', 'project',
        'category_list', 'tag_list', 'deadline', 'created_at',
    )
    list_filter = ('status', 'priority', 'tags', 'created_at')
    search_fields = ('title', 'description', 'tags__name')
    filter_horizontal = ('categories', 'tags')
    inlines = (SubTaskInline,)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Task]:
        """Задачи вместе с категориями и тегами — без N+1 в списке."""
        return (
            super()
            .get_queryset(request)
            .select_related('project')
            .prefetch_related('categories', 'tags')
        )

    @admin.display(description='Tags')
    def tag_list(self, obj: Task) -> str:
        """Теги задачи одной строкой."""
        return ', '.join(tag.name for tag in obj.tags.all()) or '—'

    @admin.display(description='Categories')
    def category_list(self, obj: Task) -> str:
        """Категории задачи одной строкой."""
        return ', '.join(category.name for category in obj.categories.all())

    @admin.display(description='Title')
    def short_title(self, obj: Task) -> str:
        """Укороченное название для списка задач."""
        if len(obj.title) > 10:
            return f'{obj.title[:10]}...'
        return obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    actions = ('mark_done',)

    def get_queryset(self, request: HttpRequest) -> QuerySet[SubTask]:
        """Подзадачи вместе с родительской задачей — без N+1."""
        return super().get_queryset(request).select_related('task')

    @admin.action(description='Mark selected as Done')
    def mark_done(self, request, queryset) -> None:
        """Переводит выбранные подзадачи в статус Done."""
        updated = queryset.update(status=Status.DONE)
        self.message_user(request, f'{updated} subtasks marked as Done.')