from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.task.views import lagacy
from apps.task.views.categories import CategoryViewSet
from apps.task.views.subtasks import (
    SubTaskDetailView,
    SubTaskListCreateView,
)
from apps.task.views.tags import TagDetailView, TagListCreateView
from apps.task.views.tasks import (
    TaskDetailView,
    TaskListCreateView,
    TaskStatisticsView,
)

app_name = 'task'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),

    path('projects/', lagacy.get_all_projects, name='project-list'),

    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/statistics/', TaskStatisticsView.as_view(),
         name='task-statistics'),
    path('tasks/<uuid:task_id>/', TaskDetailView.as_view(), name='task-detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list'),
    path('subtasks/<uuid:subtask_id>/', SubTaskDetailView.as_view(),
         name='subtask-detail'),

    path('tags/', TagListCreateView.as_view(), name='tag-list'),
    path('tags/<uuid:pk>/', TagDetailView.as_view(), name='tag-detail'),
]
