from django.db import models
from django.conf import settings


class Project(models.Model):
    TYPE_CHOICES = [
        ("back_end", "Back-end"),
        ("front_end", "Front-end"),
        ("ios", "IOS"),
        ("android", "Android")
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ("low", "LOW"),
        ("medium", "MEDIUM"),
        ("high", "HIGH")
    ]
    TYPE_CHOICES = [
        ("bug", "BUG"),
        ("feature", "FEATURE"),
        ("task", "TASK")
    ]
    STATUS_CHOICES = [
        ("to_do", "To do"),
        ("in_progress", "In progress"),
        ("finished", "Finished")
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issues_created"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues_in_project"
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to_do")
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments_created"
    )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments_in_issue"
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributors"
    )
