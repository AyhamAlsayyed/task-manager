from django.shortcuts import redirect, render

from app.models import Project, ProjectMembership


def projects_view(request):
    owner = request.user
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        if not title:
            return render(request, "app/projects.html", {"error_message": "Title is required."})
        else:
            project = Project(owner=request.user, title=title, description=description)
            project.save()
            membership = ProjectMembership(user=owner, role="O", project=project)
            membership.save()
            return redirect("app:projects")
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
