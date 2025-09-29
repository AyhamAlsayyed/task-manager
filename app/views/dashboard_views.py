from django.shortcuts import render

from app.models import Project


def dashboard_view(request):
    user = request.user
    project_count = Project.objects.filter(memberships__user=user).count()
    todo_tasks = user.tasks.filter(status="todo").count()
    completed_tasks = user.tasks.filter(status="done").count()
    inprogress_tasks = user.tasks.filter(status="inprogress").count()
    tasks_count = user.tasks.count()
    progress = 0
    if tasks_count > 0:
        progress = (completed_tasks / tasks_count) * 100

    recent_tasks = user.tasks.all().order_by("-created_at")[:5]
    recent_projects = Project.objects.filter(memberships__user=user).order_by("-created_at")[:5]
    context = {
        "user": user,
        "project_count": project_count,
        "todo_tasks": todo_tasks,
        "completed_tasks": completed_tasks,
        "inprogress_tasks": inprogress_tasks,
        "recent_tasks": recent_tasks,
        "progress": progress,
        "recent_projects": recent_projects,
    }
    return render(request, "app/dashboard.html", context)
