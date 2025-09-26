from django.shortcuts import render

from app.models import Project


def dashboard_view(request):
    user = request.user
    project_count = Project.objects.filter(memberships__user=user).count()
    task_count = user.tasks.filter(status="todo").count()
    completed_tasks = user.tasks.filter(status="done").count()
    inprogress_tasks = user.tasks.filter(status="inprogress").count()
    progress = completed_tasks / (task_count + inprogress_tasks + completed_tasks) * 100

    recent_tasks = user.tasks.all().order_by("-created_at")[:5]
    recent_projects = user.projects.all().order_by("-created_at")[:5]
    context = {
        "project_count": project_count,
        "task_count": task_count,
        "completed_tasks": completed_tasks,
        "inprogress_tasks": inprogress_tasks,
        "recent_tasks": recent_tasks,
        "progress": progress,
        "recent_projects": recent_projects,
    }
    return render(request, "app/dashboard.html", context)
