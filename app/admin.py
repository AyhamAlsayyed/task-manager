from django.contrib import admin

from .models import Comment, Project, ProjectMembership, Task, UserProfile

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(ProjectMembership)
admin.site.register(Task)
admin.site.register(Comment)
