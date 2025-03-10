from django import forms
from .models import ArtistProfile, Artwork

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