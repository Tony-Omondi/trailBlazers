from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from allauth.account.forms import LoginForm, SignupForm
from allauth.account.utils import get_user_model
from .models import ArtistProfile
from .forms import ArtistProfileForm, ArtworkForm
import logging

logger = logging.getLogger(__name__)

def is_artist(user):
    return user.is_authenticated and user.groups.filter(name="Artist").exists()

@login_required
@user_passes_test(is_artist)
def artist_dashboard(request):
    artist_profile, created = ArtistProfile.objects.get_or_create(user=request.user)
    artworks = artist_profile.artworks.all()
    return render(request, 'prof/artist_dashboard.html', {'artist_profile': artist_profile, 'artworks': artworks})

@login_required
@user_passes_test(is_artist)
def edit_artist_profile(request):
    artist_profile, created = ArtistProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ArtistProfileForm(request.POST, request.FILES, instance=artist_profile)
        if form.is_valid():
            form.save()
            return redirect('prof:artist_dashboard')
    else:
        form = ArtistProfileForm(instance=artist_profile)
    return render(request, 'prof/edit_profile.html', {'form': form})

@login_required
@user_passes_test(is_artist)
def upload_artwork(request):
    artist_profile, created = ArtistProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = artist_profile
            artwork.save()
            return redirect('prof:artist_dashboard')
    else:
        form = ArtworkForm()
    return render(request, 'prof/upload_artwork.html', {'form': form})

def artist_auth(request):
    mode = request.GET.get('mode', 'login')
    logger.info(f"Rendering artist auth page with mode: {mode}, method: {request.method}")

    # Initialize form based on mode
    if mode == 'login':
        form_class = LoginForm
    else:
        form_class = SignupForm

    if request.method == 'POST':
        if 'signup' in request.POST:
            logger.info("Processing artist signup")
            form = SignupForm(data=request.POST)
            if form.is_valid():
                try:
                    # Check if email already exists
                    email = form.cleaned_data.get('email')
                    User = get_user_model()
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "An account with this email already exists. Please log in instead.")
                        logger.info(f"Signup failed: Email {email} already exists")
                        return redirect('prof:artist_auth', mode='login')
                    user = form.save(request)
                    ArtistProfile.objects.get_or_create(user=user)
                    messages.success(request, "Successfully signed up as an artist! Please check your email to verify.")
                    logger.info(f"Artist {user.email} signed up successfully")
                    return redirect('prof:artist_auth?mode=login')  # Redirect to login after signup
                except Exception as e:
                    messages.error(request, f"Signup failed: {str(e)}")
                    logger.error(f"Artist signup error: {str(e)}")
            else:
                for error in form.errors.values():
                    messages.error(request, error[0])
                    logger.error(f"Artist signup form error: {error[0]}")
        elif 'login' in request.POST:
            logger.info("Processing artist login")
            form = LoginForm(data=request.POST, request=request)
            if form.is_valid():
                form.login(request)
                logger.info(f"Artist {form.user.email} logged in successfully")
                return redirect('prof:artist_dashboard')
            else:
                for error in form.errors.values():
                    messages.error(request, error[0])
                    logger.error(f"Artist login form error: {error[0]}")
        else:
            form = form_class()
    else:
        form = form_class()  # Fresh form on GET, no validation

    return render(request, 'prof/artist_auth.html', {'mode': mode, 'form': form})