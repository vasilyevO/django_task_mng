from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from apps.core.models import Status, TimeStampedModel, UUIDModel


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet, в котором массовое удаление тоже мягкое."""

    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        """Настоящее удаление из БД — когда оно действительно нужно."""
        return super().delete()


class CategoryManager(models.Manager):
    """Менеджер по умолчанию: «удалённые» категории не видны."""

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            is_deleted=False,
        )


class Category(UUIDModel, TimeStampedModel):
    """Категория выполнения."""

    name = models.CharField(max_length=30, verbose_name=_('Name'))
    is_deleted = models.BooleanField(
        default=False, verbose_name=_('Is deleted')
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Deleted at')
    )

    objects = CategoryManager()
    all_objects = models.Manager()  # включая «удалённые»

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']
        constraints = [
            # имя уникально только среди «живых» категорий:
            # мягко удалённое имя можно использовать снова
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(is_deleted=False),
                name='unique_active_category_name',
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление: запись остаётся в БД, но помечается удалённой."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=['is_deleted', 'deleted_at'])

    def hard_delete(self, using=None, keep_parents=False):
        """Физическое удаление записи."""
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self) -> None:
        """Возвращает мягко удалённую категорию обратно."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])


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

    @property
    def count_of_files(self) -> int:
        """Количество файлов проекта (вычисляется на лету)."""
        return self.files.count()

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
    file_path = models.FileField(
        upload_to='documents/',
        max_length=500,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'csv', 'doc', 'docx', 'xlsx'],
            ),
        ],
        verbose_name=_('File path'),
    )
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
    last_notified_status = models.CharField(
        max_length=15,
        choices=Status.choices,
        blank=True,
        editable=False,
        verbose_name=_('Last notified status'),
    )
    deadline = models.DateTimeField(verbose_name=_('Deadline'))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('Owner'),
    )

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
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name=_('Owner'),
    )

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = _('SubTask')
        verbose_name_plural = _('SubTasks')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title