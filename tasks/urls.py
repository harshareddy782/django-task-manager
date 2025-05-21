from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('mark-done/<int:task_id>/', views.mark_done, name='mark_done'),

    # Admin-only views
    path('manage/users/', views.admin_user_list, name='admin_user_list'),
    path('manage/users/<int:user_id>/tasks/', views.admin_view_tasks, name='admin_view_tasks'),
    path('manage/task/<int:task_id>/edit/', views.admin_edit_task, name='admin_edit_task'),
    path('manage/task/<int:task_id>/delete/', views.admin_delete_task, name='admin_delete_task'),
    path('manage/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
]
