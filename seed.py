"""Скрипт CRUD-операций."""

import os
from datetime import timedelta

import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import Status
from apps.task.models import SubTask, Task   


def create_records() -> None:
    """Создаёт задачу и две подзадачи к ней."""
    now = timezone.now()

    task = Task.objects.create(
        title='Prepare presentation',
        description='Prepare materials and slides for the presentation',
        status=Status.NEW,
        deadline=now + timedelta(days=3),
    )

    SubTask.objects.bulk_create([
        SubTask(
            title='Gather information',
            description='Find necessary information for the presentation',
            status=Status.NEW,
            deadline=now + timedelta(days=2),
            task=task,
        ),
        SubTask(
            title='Create slides',
            description='Create presentation slides',
            status=Status.NEW,
            deadline=now + timedelta(days=1),
            task=task,
        ),
    ])
    print(f'Created task: {task}')
    print(f'SubTasks: {task.subtasks.count()}')


def read_records() -> None:
    """Читает задачи и подзадачи по условиям."""
    print('Tasks with status New:')
    for task in Task.objects.filter(status=Status.NEW):
        print(f'  {task} — deadline {task.deadline:%Y-%m-%d}')

    print('SubTasks with status Done and expired deadline:')
    overdue = SubTask.objects.filter(
        status=Status.DONE,
        deadline__lt=timezone.now(),
    )
    for subtask in overdue:
        print(f'  {subtask} — deadline {subtask.deadline:%Y-%m-%d}')


def update_records() -> None:
    """Обновляет статус, дедлайн и описание."""
    task = Task.objects.get(title='Prepare presentation')
    task.status = Status.IN_PROGRESS
    task.save(update_fields=['status', 'updated_at'])

    gather = SubTask.objects.get(title='Gather information')
    gather.deadline = timezone.now() - timedelta(days=2)
    gather.save(update_fields=['deadline', 'updated_at'])

    slides = SubTask.objects.get(title='Create slides')
    slides.description = 'Create and format presentation slides'
    slides.save(update_fields=['description', 'updated_at'])

    print('Records updated')


def delete_records() -> None:
    """Удаляет задачу вместе с её подзадачами."""
    task = Task.objects.get(title='Prepare presentation')
    deleted_count, details = task.delete()
    print(f'Deleted objects: {deleted_count}')
    print(f'Details: {details}')


if __name__ == '__main__':
    create_records()
    read_records()
    update_records()
    read_records()
    delete_records()