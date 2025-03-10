from django.db import models
from django.contrib.auth.models import User, Group

class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_public = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    artistic_style = models.CharField(max_length=50, choices=[('abstract', 'Abstract'), ('realism', 'Realism'), ('other', 'Other')], default='other')

    def save(self, *args, **kwargs):
        if not self.pk:
            artist_group, _ = Group.objects.get_or_create(name="Artist")
            self.user.groups.add(artist_group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.user.username

class Artwork(models.Model):
    artist = models.ForeignKey(ArtistProfile, related_name='artworks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artworks/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title