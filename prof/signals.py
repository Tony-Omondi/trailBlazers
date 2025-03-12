# prof/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ArtistProfile

@receiver(post_save, sender=User)
def create_artist_profile(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name="Artist").exists():
        ArtistProfile.objects.create(user=instance)