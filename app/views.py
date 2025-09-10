from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

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
    return render(request, "app/dashboard.html")


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
