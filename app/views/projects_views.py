from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from app.models import Project, ProjectMembership, Task


def projects_view(request):
    owner = request.user
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        if not title:
            messages.error(request, "Title is required.", extra_tags="invite-member")
            return redirect("app:projects")

        project = Project(owner=owner, title=title, description=description)
        project.save()
        membership = ProjectMembership(user=owner, role="O", project=project)
        membership.save()
        messages.success(request, "Project created successfully.", extra_tags="invite-member")
        return redirect("app:projects")

    projects = Project.objects.filter(memberships__user=owner).order_by("-created_at")
    for project in projects:
        membership = ProjectMembership.objects.get(project=project, user=owner)
        project.user_role = membership.get_role_display()

    context = {
        "projects": projects,
    }
    return render(request, "app/projects.html", context)


def project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    users_in = User.objects.exclude(memberships__project=project).order_by("username")
    users = User.objects.filter(memberships__project=project)
    membership = ProjectMembership.objects.get(project=project, user=request.user)
    project.user_role = membership.role
    tasks = project.tasks.all()
    context = {
        "tasks": tasks,
        "project": project,
        "users_in": users_in,
        "users": users,
    }
    return render(request, "app/project.html", context)


def add_member_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method != "POST":
        return redirect(reverse("app:project", args=[project_id]) + "#invite-member")

    user_id = request.POST.get("user_id")
    role = request.POST.get("role")

    if not user_id:
        messages.error(request, "Please select a user.")
        return redirect(reverse("app:project", args=[project_id]) + "#invite-member")

    invited_user = get_object_or_404(User, pk=user_id)
    if ProjectMembership.objects.filter(user=invited_user, project=project).exists():
        messages.error(request, f"{invited_user.username} is already a member of this project.")
        return redirect(reverse("app:project", args=[project_id]) + "#invite-member")

    ProjectMembership.objects.create(user=invited_user, role=role, project=project)
    messages.success(request, f"{invited_user.username} has been added to the project.")
    return redirect(reverse("app:project", args=[project_id]) + "#invite-member")


def create_task_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    membership = ProjectMembership.objects.get(project=project, user=request.user)

    if not membership or membership.role != "O":
        messages.error(request, "You do not have permission to create a task.", extra_tags="create-task")
        return redirect(reverse("app:project", args=[project_id]) + "#create-task")

    if request.method == "POST":
        title = request.POST.get("title").strip()
        user_id = request.POST.get("user_id")
        deadline = request.POST.get("deadline")

        if not user_id:
            messages.error(request, "Please select a user.", extra_tags="create-task")
            return redirect(reverse("app:project", args=[project_id]) + "#create-task")

        if not title:
            messages.error(request, "Title is required.", extra_tags="create-task")
            return redirect(reverse("app:project", args=[project_id]) + "#create-task")

        if not deadline:
            messages.error(request, "Deadline is required.", extra_tags="create-task")
            return redirect(reverse("app:project", args=[project_id]) + "#create-task")

        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
        deadline_dt = timezone.make_aware(deadline_dt)

        if deadline_dt < timezone.now():
            messages.error(request, "Deadline can't be in the past.", extra_tags="create-task")
            return redirect(reverse("app:project", args=[project_id]) + "#create-task")

        assigned_user = get_object_or_404(User, pk=user_id)
        Task.objects.create(
            title=title,
            description=request.POST.get("description"),
            status=request.POST.get("status"),
            deadline=deadline,
            priority=request.POST.get("priority"),
            project=project,
            user=assigned_user,
        )
        messages.success(request, "Task created successfully.", extra_tags="create-task")
        return redirect(reverse("app:project", args=[project_id]) + "#create-task")
    return redirect(reverse("app:project", args=[project_id]) + "#create-task")
