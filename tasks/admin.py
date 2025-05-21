from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import CustomUser, Task

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'view_tasks_link')
    list_filter = ('role',)

    def view_tasks_link(self, obj):
        url = reverse('admin:tasks_task_changelist') + f'?user__id__exact={obj.id}'
        return format_html(f'<a href="{url}">View Tasks</a>')

    view_tasks_link.short_description = 'Tasks'

# Also register Task model
admin.site.register(Task)
