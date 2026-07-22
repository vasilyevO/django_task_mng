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


class Task(UUIDModel, TimeStampedModel):
    """Задача для выполнения."""

    title = models.CharField(
        max_length=100, unique=True, verbose_name=_('Title')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
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