from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from app.models import Comment, Project, ProjectMembership, Task, UserProfile


class ModelsTests(TestCase):
    """Test models creation"""

    def setUp(self):
        password = "password12345"  # nosec
        self.user = User.objects.create_user(username="testuser", password=password)

    def test_userprofile_creation(self):
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, "testuser")
        self.assertTrue(profile.avatar.name.startswith("avatars/"))
        self.assertEqual(str(profile), "testuser")

    def test_project_creation(self):
        project1 = Project.objects.create(title="p1", owner=self.user)
        project2 = Project.objects.create(title="p2", owner=self.user)
        self.assertEqual(self.user.projects.count(), 2)
        self.assertEqual(self.user.projects.last().title, "p2")
        self.assertEqual(self.user.projects.last().owner, self.user)
        self.assertEqual(str(project1), "p1")
        self.assertEqual(str(project2), "p2")

    def test_project_membership_creation(self):
        project = Project.objects.create(title="p1", owner=self.user)
        password = "password12345"  # nosec
        member = User.objects.create_user(username="testuser2", password=password)  # different username
        membership = ProjectMembership.objects.create(project=project, user=member, role="M")
        self.assertEqual(membership.project, project)
        self.assertEqual(membership.user, member)
        self.assertEqual(project.memberships.count(), 1)
        self.assertEqual(member.memberships.count(), 1)
        self.assertEqual(project.memberships.get().role, "M")

    def test_task_creation(self):
        project = Project.objects.create(title="p1", owner=self.user)
        deadline = timezone.now()
        task = Task.objects.create(
            title="t1",
            description="desc t1",
            deadline=deadline,
            project=project,
            user=self.user,
        )
        self.assertEqual(task.title, "t1")
        self.assertEqual(task.status, "todo")
        self.assertEqual(task.priority, 0)
        self.assertEqual(str(task), "t1")
        self.assertEqual(task.project, project)
        self.assertEqual(task.user, self.user)

    def test_comment_creation(self):
        project = Project.objects.create(title="p1", owner=self.user)
        deadline = timezone.now()
        task = Task.objects.create(
            title="task comment",
            description="desc",
            deadline=deadline,
            project=project,
            user=self.user,
        )
        comment = Comment.objects.create(comment="comment", task=task, author=self.user)
        self.assertEqual(comment.comment, "comment")
        self.assertEqual(comment.task, task)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(task.comments.count(), 1)
