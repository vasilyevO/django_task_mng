from django.urls import path

from apps.task import views

app_name = 'task'

urlpatterns = [
    path('projects/', views.get_all_projects, name='project-list'),
    path('tasks/', views.get_all_tasks, name='task-list'),
    path('tasks/create/', views.create_task, name='task-create'),
    path('tasks/statistics/', views.get_task_statistics, name='task-statistics'),
    path('tasks/<uuid:task_id>/', views.get_task_by_id, name='task-detail'),
    path('tags/', views.get_all_tags, name='tag-list'),
    path('tags/create/', views.create_tag, name='tag-create'),
    path('tags/<uuid:tag_id>/', views.get_tag_by_id, name='tag-detail'),
    path('tags/<uuid:tag_id>/update/', views.update_tag, name='tag-update'),
    path('tags/<uuid:tag_id>/delete/', views.delete_tag, name='tag-delete'),
]