"""Вспомогательные функции для фильтрации по query-параметрам."""
import django_filters

from apps.task.models import SubTask, Task
from rest_framework.exceptions import ValidationError

# ISO-нумерация: понедельник = 1, воскресенье = 7
WEEKDAYS = {
    'понедельник': 1, 'пн': 1, 'monday': 1, 'mon': 1, '1': 1,
    'вторник': 2, 'вт': 2, 'tuesday': 2, 'tue': 2, '2': 2,
    'среда': 3, 'ср': 3, 'wednesday': 3, 'wed': 3, '3': 3,
    'четверг': 4, 'чт': 4, 'thursday': 4, 'thu': 4, '4': 4,
    'пятница': 5, 'пт': 5, 'friday': 5, 'fri': 5, '5': 5,
    'суббота': 6, 'сб': 6, 'saturday': 6, 'sat': 6, '6': 6,
    'воскресенье': 7, 'вс': 7, 'sunday': 7, 'sun': 7, '7': 7,
}


def parse_weekday(value: str) -> int:
    """Преобразует название дня недели в ISO-номер (1–7).

    Args:
        value: название дня на русском или английском, либо число.

    Returns:
        Номер дня недели по ISO 8601.

    Raises:
        ValidationError: если день недели не распознан.
    """
    normalized = value.strip().casefold()

    if normalized not in WEEKDAYS:
        raise ValidationError({
            'weekday': (
                f'Unknown weekday: "{value}". '
                f'Use a name (понедельник / monday) or a number 1–7.'
            ),
        })

    return WEEKDAYS[normalized]

class TaskFilter(django_filters.FilterSet):
    """Фильтр задач: точный статус + диапазон по дедлайну."""

    deadline_after = django_filters.DateFilter(
        field_name='deadline', lookup_expr='date__gte',
    )
    deadline_before = django_filters.DateFilter(
        field_name='deadline', lookup_expr='date__lte',
    )

    class Meta:
        model = Task
        fields = ['status', 'deadline_after', 'deadline_before']


class SubTaskFilter(django_filters.FilterSet):
    """Фильтр подзадач: точный статус + диапазон по дедлайну."""

    deadline_after = django_filters.DateFilter(
        field_name='deadline', lookup_expr='date__gte',
    )
    deadline_before = django_filters.DateFilter(
        field_name='deadline', lookup_expr='date__lte',
    )

    class Meta:
        model = SubTask
        fields = ['status', 'deadline_after', 'deadline_before']