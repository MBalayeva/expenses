from django.contrib.auth.models import User
from .models import UserPreferences
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User) 
def create_preference(sender, instance, created, **kwargs):
    if created:
        UserPreferences.objects.create(user=instance)
   
@receiver(post_save, sender=User) 
def save_preference(sender, instance, **kwargs):
        instance.userpreferences.save()