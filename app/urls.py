from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("edit_profile/", views.edit_profile_view, name="edit_profile"),
    path("projects/", views.projects_view, name="projects"),
    path("projects/<int:project_id>/", views.project_view, name="project"),
    path("projects/<int:project_id>/create-task", views.create_task_view, name="create_task"),
    path("projects/<int:project_id>/add-member", views.add_member_view, name="add_member"),
    path("tasks/", views.tasks_view, name="tasks"),
]
