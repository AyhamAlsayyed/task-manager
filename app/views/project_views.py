from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from app.models import Project, ProjectMembership


def project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    error_message = None
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role = request.POST.get("role")

        if user_id:
            invited_user = get_object_or_404(User, pk=user_id)
            if ProjectMembership.objects.filter(user=invited_user, project=project).exists():
                error_message = f"{invited_user.username} is already a member of this project."
                return redirect("app:project", project_id=project_id)
            else:
                membership = ProjectMembership(user=invited_user, role=role, project=project)
                membership.save()
        else:
            error_message = "Please select a user."

    users = User.objects.exclude(memberships__project=project).order_by("username")
    tasks = project.tasks.all()
    membership = ProjectMembership.objects.get(project=project, user=request.user)
    project.user_role = membership.role

    context = {
        "tasks": tasks,
        "project": project,
        "users": users,
        "error_message": error_message,
    }
    return render(request, "app/project.html", context)
