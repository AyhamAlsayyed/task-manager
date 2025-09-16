from django.shortcuts import render


def dashboard_view(request):
    user = request.user
    project_count = user.projects.count()
    task_count = user.tasks.filter(status="todo").count()
    completed_tasks = user.tasks.filter(status="done").count()
    inprogress_tasks = user.tasks.filter(status="inprogress").count()

    recent_tasks = user.tasks.all().order_by("-created_at")[:5]
    context = {
        "project_count": project_count,
        "task_count": task_count,
        "completed_tasks": completed_tasks,
        "inprogress_tasks": inprogress_tasks,
        "recent_tasks": recent_tasks,
    }
    return render(request, "app/dashboard.html", context)
