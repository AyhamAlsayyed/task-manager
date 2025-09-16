from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


# Login, logout, signup views
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


def home_view(request):
    return render(request, "app/home.html")
