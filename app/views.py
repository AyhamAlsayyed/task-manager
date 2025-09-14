from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from app.models import Project, ProjectMembership

# Create your views here.


def home_view(request):
    return render(request, "app/home.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
        else:
            return render(
                request,
                "app/login.html",
                {"form": form, "error_message": "User name or Password are incorrect."},
            )
    else:
        form = AuthenticationForm()
    return render(request, "app/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, "app/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("app:home")


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


def profile_view(request):
    return render(request, "app/profile.html")


def edit_profile_view(request):
    user = request.user
    profile = user.userprofile

    if request.method == "POST":
        avatar = request.FILES.get("avatar")

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()

        profile.bio = request.POST.get("bio")

        avatar = request.FILES.get("avatar")
        if avatar:
            profile.avatar = avatar
        profile.save()

        return redirect("app:home")

    return render(request, "app/profile.html")


def projects_view(request):
    owner = request.user
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        if title:
            project = Project(owner=request.user, title=title, description=description)
            project.save()
            membership = ProjectMembership(user=owner, role="O", project=project)
            membership.save()
            return redirect("app:projects")
        else:
            error_message = "Title is required."
    else:
        error_message = None

    projects = Project.objects.filter(memberships__user=owner).order_by("-created_at")
    for project in projects:
        membership = ProjectMembership.objects.get(project=project, user=owner)
        project.user_role = membership.get_role_display()

    context = {
        "projects": projects,
        "error_message": error_message,
    }
    return render(request, "app/projects.html", context)


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
    tasks = project.tasks.all().filter(project_id=project_id)
    membership = ProjectMembership.objects.get(project=project, user=request.user)
    project.user_role = membership.role
    context = {
        "tasks": tasks,
        "project": project,
        "users": users,
        "error_message": error_message,
    }
    return render(request, "app/project.html", context)
