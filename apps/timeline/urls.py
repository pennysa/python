from django.urls import path
from . import views

app_name = 'timeline'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('tasks/', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/', views.get_task, name='get_task'),
    path('toggle/<int:task_id>/', views.toggle_done, name='toggle_done'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
