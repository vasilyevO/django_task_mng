from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import Status, TimeStampedModel, UUIDModel


class Category(UUIDModel, TimeStampedModel):
    """Категория выполнения."""

    name = models.CharField(
        max_length=30, unique=True, verbose_name=_('Name')
    )

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Priority(models.TextChoices):
    """Приоритет задачи — ярлык, своей таблицы нет."""

    LOW = 'low', _('Low')
    MEDIUM = 'medium', _('Medium')
    HIGH = 'high', _('High')

class Project(UUIDModel, TimeStampedModel):
    """Проект, объединяющий задачи."""

    name = models.CharField(
        max_length=100, unique=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        db_table = 'task_manager_project'
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name


class Tag(UUIDModel, TimeStampedModel):
    """Метка задачи."""

    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

    class Meta:
        db_table = 'task_manager_tag'
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class ProjectFile(UUIDModel, TimeStampedModel):
    """Файл, прикреплённый к проекту."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_('Project'),
    )
    file_name = models.CharField(max_length=255, verbose_name=_('File name'))
    file_path = models.CharField(max_length=500, verbose_name=_('File path'))

    class Meta:
        db_table = 'task_manager_project_file'
        verbose_name = _('Project file')
        verbose_name_plural = _('Project files')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.file_name


class Task(UUIDModel, TimeStampedModel):
    """Задача для выполнения."""

    title = models.CharField(max_length=100, unique=True, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    project = models.ForeignKey(  # ← НОВОЕ
        Project,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks',
        verbose_name=_('Project'),
    )
    tags = models.ManyToManyField(  # ← НОВОЕ
        Tag,
        blank=True,
        related_name='tasks',
        verbose_name=_('Tags'),
    )
    priority = models.CharField(  # ← НОВОЕ
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name=_('Priority'),
    )

    categories = models.ManyToManyField(
        Category,
        related_name='tasks',
        blank=True,
        verbose_name=_('Categories'),
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name=_('Status'),
    )
    deadline = models.DateTimeField(verbose_name=_('Deadline'))

    class Meta:
        db_table = 'task_manager_task'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


class SubTask(UUIDModel, TimeStampedModel):
    """Отдельная часть основной задачи."""

    title = models.CharField(
        max_length=100, unique=True, verbose_name=_('Title')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name=_('Task'),
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name=_('Status'),
    )
    deadline = models.DateTimeField(verbose_name=_('Deadline'))

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = _('SubTask')
        verbose_name_plural = _('SubTasks')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title