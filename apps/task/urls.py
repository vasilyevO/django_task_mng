from django.urls import path

from apps.task import views
from apps.task.views.subtasks import (
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateView,
)
from apps.task.views.tags import TagDetailView, TagListCreateView
from apps.task.views.tasks import (
    TaskDetailView,
    TaskListCreateView,
    TaskStatisticsView,
)

app_name = 'task'

urlpatterns = [
    # --- ещё не переведено на APIView ---
    path('projects/', views.get_all_projects, name='project-list'),

    # --- задачи ---
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path(
        'tasks/statistics/',
        TaskStatisticsView.as_view(),
        name='task-statistics',
    ),
    path('tasks/<uuid:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # --- теги ---
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<uuid:pk>/', TagDetailView.as_view(), name='tag-detail'),

    # --- подзадачи ---
    path(
        'subtasks/',
        SubTaskListCreateView.as_view(),
        name='subtask-list-create',
    ),
    path(
        'subtasks/<uuid:pk>/',
        SubTaskDetailUpdateDeleteView.as_view(),
        name='subtask-detail',
    ),
]