from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Artwork
from .forms import ArtworkForm

@login_required
def profile_view(request):
    artist_profile = request.user.artistprofile
    artworks = artist_profile.artworks.all()
    return render(request, 'prof/prof.html', {'artworks': artworks})

@login_required
def upload_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user.artistprofile
            artwork.save()
            return redirect('prof')
    else:
        form = ArtworkForm()
    return render(request, 'prof/upload.html', {'form': form})