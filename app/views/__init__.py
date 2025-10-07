# flake8: noqa: F403, F401
from .auth_views import login_view, logout_view, signup_view
from .dashboard_views import dashboard_view
from .home_view import home_view
from .profile_views import edit_profile_view, profile_view
from .projects_views import (
    add_member_view,
    create_task_view,
    edit_project_view,
    project_view,
    projects_view,
)
from .tasks_views import edit_task_view, task_view, tasks_view
