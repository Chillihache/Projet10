from django.db.models.signals import post_save
from django.dispatch import receiver
from projecthub.models import Project, Contribute


@receiver(post_save, sender=Project)
def create_contribute_after_project_created(sender, instance, created, **kwargs):
    if created:
        Contribute.objects.get_or_create(
            author=instance.author,
            project=instance
        )
