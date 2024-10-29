from django.db import models
from django.conf import settings
import uuid


class TimeStampMixin(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Project(TimeStampMixin, models.Model):
    TYPE_CHOICES = [
        ("back_end", "Back-end"),
        ("front_end", "Front-end"),
        ("ios", "IOS"),
        ("android", "Android")
    ]
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Issue(TimeStampMixin, models.Model):
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
    name = models.CharField(max_length=100)
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
    assigned_contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues"
    )

    def __str__(self):
        return self.name


class Comment(TimeStampMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


class Contribute(TimeStampMixin, models.Model):
    class Meta:
        unique_together = ("author", "project")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributors"
    )

