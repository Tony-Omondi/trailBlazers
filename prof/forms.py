from django import forms
from .models import ArtistProfile, Artwork, Order

class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields = [
            'full_name', 'bio', 'profile_picture', 'phone_number',
            'email_public', 'location', 'linkedin_url', 'facebook_url',
            'instagram_url', 'artistic_style'
        ]

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image', 'price', 'is_available']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer_name', 'buyer_email', 'buyer_phone']
        widgets = {
            'buyer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'buyer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'buyer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }