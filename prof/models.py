from django.db import models
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail

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

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='orders')
    transaction_id = models.CharField(max_length=100, unique=True)
    buyer_name = models.CharField(max_length=100)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=15, blank=True, null=True)
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_completed and not self.pk:  # Only send emails on creation of completed order
            # Notify buyer
            send_mail(
                subject=f"KibraConnect: Your Order for {self.artwork.title}",
                message=f"Dear {self.buyer_name},\n\nThank you for your purchase of '{self.artwork.title}' for KES {self.amount}. Your transaction ID is {self.transaction_id}.\n\nBest regards,\nKibraConnect Team",
                from_email='no-reply@kibraconnect.com',
                recipient_list=[self.buyer_email],
                fail_silently=False,
            )
            # Notify artist
            send_mail(
                subject=f"KibraConnect: New Order for Your Artwork - {self.artwork.title}",
                message=f"Dear {self.artist.full_name or self.artist.user.username},\n\nYour artwork '{self.artwork.title}' has been purchased by {self.buyer_name} for KES {self.amount}. Transaction ID: {self.transaction_id}.\n\nBest regards,\nKibraConnect Team",
                from_email='no-reply@kibraconnect.com',
                recipient_list=[self.artist.user.email],
                fail_silently=False,
            )
            # Notify admin
            send_mail(
                subject=f"KibraConnect: New Order Notification - {self.artwork.title}",
                message=f"Admin,\n\nA new order has been placed for '{self.artwork.title}' by {self.buyer_name}. Amount: KES {self.amount}, Transaction ID: {self.transaction_id}.\n\nBest regards,\nKibraConnect System",
                from_email='no-reply@kibraconnect.com',
                recipient_list=['otienotony598@gmail.com'],
                fail_silently=False,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.transaction_id} for {self.artwork.title}"