from django.contrib import admin
from .models import Task, Project

class   TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
# Register your models here.



admin.site.register(Task, TaskAdmin)
admin.site.register(Project)