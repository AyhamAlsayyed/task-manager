from django.db.models import (
    Case,
    Count,
    ExpressionWrapper,
    F,
    FloatField,
    Q,
    Value,
    When,
)
from django.shortcuts import render

from app.models import Project, ProjectMembership


def dashboard_view(request):
    user = request.user
    project_count = Project.objects.filter(memberships__user=user).count()
    todo_tasks = user.tasks.filter(status="todo").count()
    completed_tasks = user.tasks.filter(status="done").count()
    inprogress_tasks = user.tasks.filter(status="inprogress").count()

    recent_tasks = user.tasks.all().order_by("-created_at")[:5]
    recent_memberships = (
        ProjectMembership.objects.filter(user=user)
        .select_related("project", "project__owner")
        .annotate(
            total_tasks=Count("project__tasks", distinct=True),
            completed_tasks=Count(
                "project__tasks",
                filter=Q(project__tasks__status="done"),
                distinct=True,
            ),
        )
        .annotate(
            progress=Case(
                When(total_tasks=0, then=Value(0.0)),
                default=ExpressionWrapper(
                    100.0 * F("completed_tasks") / F("total_tasks"),
                    output_field=FloatField(),
                ),
            )
        )
        .order_by("-project__created_at")[:5]
    )

    context = {
        "user": user,
        "project_count": project_count,
        "todo_tasks": todo_tasks,
        "completed_tasks": completed_tasks,
        "inprogress_tasks": inprogress_tasks,
        "recent_tasks": recent_tasks,
        "recent_memberships": recent_memberships,
    }
    return render(request, "app/dashboard.html", context)
