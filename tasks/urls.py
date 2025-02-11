from django.urls import path
from .views import create_task, task_detail, filter_tasks_by_status, mark_task_completed

urlpatterns = [
    path('', create_task, name='create_task'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('filter/', filter_tasks_by_status, name='filter_tasks_by_status'),
    path('<int:pk>/complete/', mark_task_completed, name='mark_task_completed')
]
