from django.db.models.signals import post_save
from django.dispatch import receiver
from functools import wraps
from django.contrib.auth.models import User

from .models import UserProfile

def prevent_recursion(func):
    """ Decorator
        Prevent Recursion inside Post Save Signal
    """
    @wraps(func)
    def no_recursion(sender, instance=None, **kwargs):
        if not instance:
            return

        # if there is _dirty, return
        if hasattr(instance, '_dirty'):
            return
        func(sender, instance=instance, **kwargs)
        try:
            # there is dirty, lets save
            instance._dirty = True
            instance.save()
        finally:
            del instance._dirty
    return no_recursion


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Create User Profile For User """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


