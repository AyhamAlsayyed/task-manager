from django.shortcuts import render


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
