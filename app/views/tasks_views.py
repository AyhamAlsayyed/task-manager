from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from app.models import Task


def tasks_view(request):
    user = request.user
    tasks = user.tasks.all()

    if request.method != "GET":
        context = {
            "tasks": tasks,
        }
        return render(request, "app/tasks.html", context)

    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    deadline = request.GET.get("deadline", "")

    if query:
        tasks = tasks.filter(title__icontains=query) | tasks.filter(description__icontains=query)

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority={"L": 0, "M": 1, "H": 2}[priority])

    if deadline:
        tasks = tasks.filter(deadline=deadline)

    context = {
        "tasks": tasks,
    }
    return render(request, "app/tasks.html", context)


def task_view(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    users_in = task.project.members.all()

    context = {
        "task": task,
        "users_in": users_in,
    }
    return render(request, "app/task.html", context)


def edit_task_view(request, task_id):
    anchor = "edit-task"
    task = get_object_or_404(Task, pk=task_id)
    title = request.POST.get("title").strip()
    user_id = request.POST.get("user_id")
    deadline = request.POST.get("deadline")

    if not user_id:
        error_message = "User_id is required"
        return render(request, "app/task.html", task_context(task, error_message, anchor))

    if not title:
        error_message = "Title is required"
        return render(request, "app/task.html", task_context(task, error_message, anchor))

    if not deadline:
        error_message = "Deadline is required"
        return render(request, "app/task.html", task_context(task, error_message, anchor))

    deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
    deadline_dt = timezone.make_aware(deadline_dt)

    if deadline_dt < timezone.now():
        error_message = "Deadline can't be in the past"
        return render(request, "app/task.html", task_context(task, error_message, anchor))

    assigned_user = get_object_or_404(User, pk=user_id)

    task.title = title
    task.description = request.POST.get("description")
    task.status = request.POST.get("status")
    task.priority = request.POST.get("priority")
    task.deadline = deadline_dt
    task.users = assigned_user
    task.save()

    return redirect(reverse("app:task", args=[task.id]))


def task_context(task, error_message=None, anchor=None):
    users_in = task.project.members.all()
    context = {
        "task": task,
        "users_in": users_in,
        "error_message": error_message,
        "anchor": anchor,
    }
    return context
