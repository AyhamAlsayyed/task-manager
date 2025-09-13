from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars/", default="avatars/default.png")
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title


class ProjectMembership(models.Model):
    role_choices = [("O", "owner"), ("M", "member")]
    role = models.CharField(max_length=1, choices=role_choices, default="M")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")


class Task(models.Model):
    status_choices = [
        ("todo", "TO do"),
        ("inprogress", "IN progress"),
        ("done", "DONE"),
    ]

    priority_choices = [
        (0, "low"),
        (1, "medium"),
        (2, "high"),
    ]
    Tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=status_choices, default="todo")
    priority = models.IntegerField(choices=priority_choices, default=0)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
