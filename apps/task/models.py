from django.db import models
from django.db.models.functions import TruncDate
from django.core.exceptions import ValidationError
from django.utils import timezone


class Status(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in_progress', 'In progress'
    PENDING = 'pending', 'Pending'
    BLOCKED = 'blocked', 'Blocked'
    DONE = 'done', 'Done'


class Category(models.Model):
    """Категория выполнения."""

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    """Задача для выполнения."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(
        Category,
        related_name='tasks',
        blank=True,
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
    )
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        """Проверяет уникальность названия в пределах даты создания.

        Raises:
            ValidationError: Задача с таким названием уже есть на эту дату.
        """
        target_date = (
            self.created_at.date() if self.created_at else timezone.localdate()
        )
        duplicates = Task.objects.filter(
            title=self.title,
            created_at__date=target_date,
        )
        if self.pk:
            duplicates = duplicates.exclude(pk=self.pk)
        if duplicates.exists():
            raise ValidationError(
                {'title': 'Задача с таким названием уже создана на эту дату.'}
            )


class SubTask(models.Model):
    """Отдельная часть основной задачи."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks',
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
    )
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title