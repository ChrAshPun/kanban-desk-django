from django.urls import path
from .views import ProjectCreateView, ProjectUpdateView, ProjectDeleteView, ProjectKanbanView, ProjectSettingsView, TaskCreateView, TaskUpdateView, TaskDeleteView

app_name = 'project'

urlpatterns = [
  path('new/', ProjectCreateView.as_view(), name='create'),
  path('<int:pk>/update/', ProjectUpdateView.as_view(), name='update'),
  path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete'),
  path('<int:pk>/kanban/', ProjectKanbanView.as_view(), name='kanban'),
  path('<int:pk>/settings/', ProjectSettingsView.as_view(), name='settings'),
  path('<int:project_pk>/task/new/', TaskCreateView.as_view(), name='task_create'),
  path('<int:project_pk>/task/<int:task_pk>/update/', TaskUpdateView.as_view(), name='task_update'),
  path('<int:project_pk>/task/<int:task_pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]