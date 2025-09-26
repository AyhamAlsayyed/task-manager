from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


# Login, logout, signup views
def login_view(request):
    if request.method != "POST":
        form = AuthenticationForm()
        return render(request, "app/login.html", {"form": form})

    form = AuthenticationForm(request, data=request.POST)
    if not form.is_valid():
        return render(
            request,
            "app/login.html",
            {"form": form, "error_message": "User name or Password are incorrect."},
        )

    user = form.get_user()
    login(request, user)
    return redirect("/")


def signup_view(request):
    if request.method != "POST":
        form = UserCreationForm()
        return render(request, "app/signup.html", {"form": form})

    form = UserCreationForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return render(request, "app/signup.html", {"form": form})

    user = form.save()
    login(request, user)
    return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("app:login")
