from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from accounts.models import UserProfile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            user_profile = UserProfile.objects.create(user=instance)
        except Exception as error:
            print("\nSIGNAL ERROR: ", error, "\n")