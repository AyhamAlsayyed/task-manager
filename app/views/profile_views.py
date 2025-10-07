from django.shortcuts import redirect, render


def profile_view(request):
    return render(request, "app/profile.html")


def edit_profile_view(request):
    user = request.user
    profile = user.userprofile

    if request.method != "POST":
        return render(request, "app/profile.html")

    avatar = request.FILES.get("avatar")
    user.username = request.POST.get("username")
    user.email = request.POST.get("email")
    user.save()

    profile.bio = request.POST.get("bio")

    if avatar:
        profile.avatar = avatar
    profile.save()

    return redirect("app:home")
