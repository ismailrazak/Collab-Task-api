from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def username_generation(sender, instance, **kwargs):

    if not instance.username:
        username = f"{instance.first_name}_{instance.last_name}"
        counter = 0
        while get_user_model().objects.filter(username=username).exists():
            username = f"{instance.first_name}_{instance.last_name}_{counter}"
            counter += 1
        instance.username = username
