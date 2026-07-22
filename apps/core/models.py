import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Отметки времени создания и обновления."""

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated at')
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Первичный ключ UUID вместо автоинкремента."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class Status(models.TextChoices):
    """Статус выполнения — общий для задач и подзадач."""

    NEW = 'new', _('New')
    IN_PROGRESS = 'in_progress', _('In progress')
    PENDING = 'pending', _('Pending')
    BLOCKED = 'blocked', _('Blocked')
    DONE = 'done', _('Done')