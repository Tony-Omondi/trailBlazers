from django.db import models
from django.contrib.auth.models import User, Group

class RegularUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country_of_origin = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            normal_group, _ = Group.objects.get_or_create(name="Normal User")
            self.user.groups.add(normal_group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    

from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="destinations/")

    def __str__(self):
        return self.name
