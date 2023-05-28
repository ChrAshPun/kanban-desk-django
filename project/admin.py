from django.contrib import admin
from .models import Project, Task

class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Project._meta.fields]

admin.site.register(Project, ProjectAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]

admin.site.register(Task, TaskAdmin)
