# tours/forms.py
from django import forms
from .models import Tour, TimeSlot

class BookingForm(forms.Form):
    date_time = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),  # Set dynamically in view
        label="Date & Time 🌷",
        empty_label="Select a time slot",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    group_size = forms.ChoiceField(
        choices=[('single', 'Just Me!'), ('couple', 'Us Two!'), ('group', 'A Fun Group!')],
        label="Travelers",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tour_duration = forms.ChoiceField(
        choices=[('half_day', 'Half-Day'), ('full_day', 'Full-Day'), ('custom', 'Custom')],
        label="Duration",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tour_type = forms.ChoiceField(
        choices=[('walking', 'Walking Tour'), ('boda_boda', 'Boda Boda')],
        label="Type",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    meeting_point = forms.ChoiceField(
        choices=[('sarangombe', 'Sarang’ombe'), ('hotel_pickup', 'Hotel Pickup')],
        label="Meeting Point",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    customer_name = forms.CharField(
        label="Your Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    customer_email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    customer_phone = forms.CharField(
        label="Phone",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, tour=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tour:
            self.fields['date_time'].queryset = tour.available_slots.filter(is_booked=False)