from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.task'
    verbose_name = 'Tasks'

    def ready(self):
        import apps.task.signals  # noqa: F401
