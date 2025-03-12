from django.contrib import admin
from .models import Guide, Tour, TimeSlot, Booking

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'linkedin_url', 'instagram_url', 'facebook_url')
    search_fields = ('full_name', 'email')

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'guide', 'price', 'base_duration')
    search_fields = ('name',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('tour', 'start_time', 'is_booked')
    list_filter = ('is_booked',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('tour', 'customer_name', 'customer_email', 'amount', 'is_completed', 'booked_at')
    search_fields = ('customer_name', 'customer_email', 'transaction_id')
    list_filter = ('is_completed', 'booked_at')