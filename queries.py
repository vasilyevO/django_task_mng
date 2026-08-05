"""Скрипт ORM-запросов."""

import os

import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.task.models import Project


def projects_created_this_month() -> None:
    """Выводит проекты, созданные в текущем месяце."""
    now = timezone.localtime()

    projects = Project.objects.filter(
        created_at__year=now.year,
        created_at__month=now.month,
    )

    if projects:
        for project in projects:
            print(f'{project.name} — {project.created_at}')
    else:
        print('Проектов за текущий месяц нет')


if __name__ == '__main__':
    projects_created_this_month()
