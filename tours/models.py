from django.db import models
from django.core.mail import send_mail
from django.utils import timezone

class Guide(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='guides/', blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name

class TimeSlot(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='available_slots')
    start_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.tour.name}"

class Tour(models.Model):
    DESTINATIONS = (
        ('guided_city_walk', 'Guided City Walk'),
        ('cultural_heritage', 'Cultural & Heritage Tour'),
        ('street_food', 'Street Food Experience'),
        ('art_graffiti', 'Art & Graffiti Tour'),
        ('nightlife', 'Nightlife & Entertainment Tour'),
    )
    DURATIONS = (
        ('half_day', 'Half-Day'),
        ('full_day', 'Full-Day'),
        ('custom', 'Custom'),
    )
    TOUR_TYPES = (
        ('walking', 'Walking Tour'),
        ('boda_boda', 'Boda Boda (Motorbike)'),
    )
    MEETING_POINTS = (
        ('sarangombe', 'Meeting at Sarang’ombe'),
        ('hotel_pickup', 'Hotel Pickup'),
    )

    name = models.CharField(max_length=100, choices=DESTINATIONS)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    featured_image = models.ImageField(upload_to='featured/', blank=True, null=True)
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True)
    base_duration = models.CharField(max_length=50, choices=DURATIONS, default='half_day')
    estimated_start_time = models.TimeField(default='09:00:00')
    estimated_end_time = models.TimeField(default='12:00:00')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)

    def __str__(self):
        return self.name

class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    group_size = models.CharField(max_length=20, choices=(('single', 'Single'), ('couple', 'Couple'), ('group', 'Group')), default='single')
    tour_duration = models.CharField(max_length=50, choices=Tour.DURATIONS, default='half_day')
    tour_type = models.CharField(max_length=20, choices=Tour.TOUR_TYPES, default='walking')
    meeting_point = models.CharField(max_length=50, choices=Tour.MEETING_POINTS, default='sarangombe')
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    merchant_reference = models.CharField(max_length=100, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    booked_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk and self.is_completed and not self._state.adding:  # On update when completed
            self.notify_guide()
            self.notify_customer()
        super().save(*args, **kwargs)

    def notify_guide(self):
        if self.tour.guide and self.tour.guide.email:
            subject = f"KibraConnect: You’re Guiding {self.tour.name}"
            message = (
                f"Dear {self.tour.guide.full_name},\n\n"
                f"You’ve been assigned to guide a tour!\n"
                f"Tour: {self.tour.name}\n"
                f"Date & Time: {self.time_slot.start_time.strftime('%Y-%m-%d %H:%M')}\n"
                f"Group Size: {self.group_size}\n"
                f"Duration: {self.tour_duration}\n"
                f"Type: {self.tour_type}\n"
                f"Meeting Point: {self.meeting_point}\n\n"
                f"Get ready for a sweet adventure! 🌸\n"
                f"KibraConnect Team"
            )
            send_mail(subject, message, 'nitonito598@gmail.com', [self.tour.guide.email], fail_silently=False)

    def notify_customer(self):
        subject = f"KibraConnect: Your Tour Booking for {self.tour.name}"
        message = (
            f"Dear {self.customer_name},\n\n"
            f"Thank you for booking '{self.tour.name}' for KES {self.amount}!\n"
            f"Date & Time: {self.time_slot.start_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"Transaction ID: {self.transaction_id}\n\n"
            f"See you soon! 🌷\n"
            f"KibraConnect Team"
        )
        send_mail(subject, message, 'nitonito598@gmail.com', [self.customer_email], fail_silently=False)

    def __str__(self):
        return f"{self.tour.name} - {self.time_slot.start_time}"