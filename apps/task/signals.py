from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from apps.core.models import Status
from apps.task.models import Task


@receiver(pre_save, sender=Task)
def remember_previous_status(sender, instance: Task, **kwargs) -> None:
    """Запоминает статус задачи до сохранения."""
    if instance._state.adding:
        instance._previous_status = None
        return
    instance._previous_status = (
        Task.objects.filter(pk=instance.pk)
        .values_list('status', flat=True)
        .first()
    )


@receiver(post_save, sender=Task)
def notify_owner_on_status_change(
    sender, instance: Task, created: bool, **kwargs,
) -> None:
    """Письмо владельцу, когда задача сменила статус или закрылась."""
    if created:
        return

    previous = getattr(instance, '_previous_status', None)
    current = instance.status
    if previous is None or previous == current:
        return
    if instance.last_notified_status == current:
        return

    owner = instance.owner
    if owner is None or not owner.email:
        return

    Task.objects.filter(pk=instance.pk).update(last_notified_status=current)
    instance.last_notified_status = current

    context = {
        'user': owner,
        'task': instance,
        'old_status': Status(previous).label,
        'new_status': Status(current).label,
        'is_closed': current == Status.DONE,
    }
    subject = (
        f'Задача «{instance.title}» закрыта'
        if context['is_closed']
        else f'Задача «{instance.title}»: статус изменён'
    )
    message = render_to_string('emails/task_status_changed.txt', context)

    transaction.on_commit(lambda: send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[owner.email],
        fail_silently=True,
    ))
