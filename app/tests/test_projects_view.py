from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from app.models import Project


class ProjectsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        password = "password12345"  # nosec
        self.user = User.objects.create_user(username="testuser", password=password)
        self.client.login(username="testuser", password=password)

    def test_projects_loads(self):
        response = self.client.get(reverse("app:projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Projects")

    def test_create_valid_project(self):
        response = self.client.post(
            reverse("app:projects"),
            {
                "title": "My Project",
                "description": "My Description",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Project.objects.filter(title="My Project").exists())

    def test_create_invalid_project(self):
        """Create a project with an invalid title."""
        response = self.client.post(
            reverse("app:projects"),
            {
                "title": "",
                "description": "My Description",
            },
            follow=True,
        )
        self.assertEqual(Project.objects.count(), 0)
        self.assertContains(response, "Title is required")
