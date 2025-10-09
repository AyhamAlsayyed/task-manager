from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from app.models import Project, ProjectMembership, Task


def projects_view(request):
    user = request.user
    if request.method != "POST":
        projects = (
            ProjectMembership.objects.filter(user=user).select_related("project").order_by("-project__created_at")
        )

        context = {
            "projects": projects,
        }
        return render(request, "app/projects.html", context)

    title = request.POST.get("title")
    description = request.POST.get("description")

    if not title:
        error_message = "Title is required"
        return render(request, "app/projects.html", {"error_message": error_message})

    with transaction.atomic():
        project = Project(owner=user, title=title, description=description)
        project.save()
        membership = ProjectMembership(user=user, role="O", project=project)
        membership.save()
    return redirect(reverse("app:projects"))


def project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, "app/project.html", project_context(project, request.user))


def add_member_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    anchor = "add-member"
    if request.method != "POST":
        return redirect(reverse("app:project", args=[project_id]) + "#invite-member")

    user_id = request.POST.get("user_id")
    role = request.POST.get("role")

    if not user_id:
        error_message = "User_id is required"
        return render(request, "app/project.html", project_context(project, request.user, error_message, anchor))

    invited_user = get_object_or_404(User, pk=user_id)
    if ProjectMembership.objects.filter(user=invited_user, project=project).exists():
        error_message = f"{invited_user.username} is already a member of this project."
        return render(request, "app/project.html", project_context(project, request.user, error_message, anchor))

    ProjectMembership.objects.create(user=invited_user, role=role, project=project)
    return redirect(reverse("app:project", args=[project_id]) + "#invite-member")


def create_task_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    membership = ProjectMembership.objects.get(project=project, user=request.user)
    anchor = "create-task"

    if not membership or (membership.role != "O" and membership.role != "A"):
        error_message = "You don't have permission to create tasks"
        return render(request, "app/project.html", project_context(project, request.user, error_message, anchor))

    if request.method != "POST":
        return redirect(reverse("app:project", args=[project_id]) + "#create-task")

    title = request.POST.get("title").strip()
    user_id = request.POST.get("user_id")
    deadline = request.POST.get("deadline")

    if not user_id:
        error_message = "User_id is required"
        return render(request, "app/project.html", project_context(project, request.user, error_message, anchor))

    if not title:
        error_message = "Title is required"
        return render(request, "app/project.html", project_context(project, request.user, error_message, anchor))

    if not deadline:
        error_message = "Deadline is required"
        return render(request, "app/project.html", project_context(project, request.user, error_message, anchor))

    deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
    deadline_dt = timezone.make_aware(deadline_dt)

    if deadline_dt < timezone.now():
        error_message = "Deadline can't be in the past"
        return render(request, "app/project.html", project_context(project, request.user, error_message, anchor))
    with transaction.atomic():
        assigned_user = get_object_or_404(User, pk=user_id)
        Task.objects.create(
            title=title,
            description=request.POST.get("description"),
            status="To Do",
            deadline=deadline,
            priority=request.POST.get("priority"),
            project=project,
            user=assigned_user,
        )

        if assigned_user and assigned_user.email:
            send_mail(
                subject="New Task assigned",
                message=f"You have a new task: {title} in project {project.title}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[assigned_user.email],
                fail_silently=False,
            )
    return redirect(reverse("app:project", args=[project_id]) + "#create-task")


def edit_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method != "POST":
        return render(request, "app/edit_project.html", {"project": project})

    title = request.POST.get("title")
    description = request.POST.get("description")

    if not title:
        error_message = "Title is required"
        return render(request, "app/project.html", project_context(project, request.user, error_message))

    project.title = title
    project.description = description
    project.save()
    return redirect(reverse("app:project", args=[project_id]))


def project_context(project, user, error_message=None, anchor=None):
    tasks = project.tasks.all()
    users_in = User.objects.exclude(memberships__project=project).order_by("username")
    users = User.objects.filter(memberships__project=project)
    membership = ProjectMembership.objects.get(project=project, user=user)
    project.user_role = membership.role
    return {
        "tasks": tasks,
        "project": project,
        "users_in": users_in,
        "users": users,
        "error_message": error_message,
        "anchor": anchor,
    }
