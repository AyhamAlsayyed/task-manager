from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from app.models import Project

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
    task_count = user.tasks.count()
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

        return redirect("app:profile")

    return render(request, "app/profile.html")


def projects_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        if title:
            project = Project(owner=request.user, title=title, description=description)
            project.save()
            return redirect("app:projects")
        else:
            error_message = "Title is required."
    else:
        error_message = None

    user = request.user
    projects = user.projects.all().order_by("-created_at")

    context = {
        "projects": projects,
        "error_message": error_message,
    }
    return render(request, "app/projects.html", context)


def project_view(request, project_id):
    return render(request, "app/project.html", {"project_id": project_id})
