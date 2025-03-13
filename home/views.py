from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from allauth.account.forms import LoginForm, SignupForm
from allauth.account.utils import get_user_model
from prof.models import ArtistProfile, Artwork
from home.models import RegularUserProfile
from home.models import Destination  # Ensure this import is included
import logging
from tours.models import Guide

logger = logging.getLogger(__name__)

def is_artist(user):
    return user.is_authenticated and user.groups.filter(name="Artist").exists()

def is_normal_user(user):
    return user.is_authenticated and user.groups.filter(name="Normal User").exists()

def home(request):
    # Fetch all guides from the database
    guides = Guide.objects.all()
    
    # Existing context data
    context = {
        'is_artist': is_artist(request.user),
        'is_normal_user': is_normal_user(request.user),
        'latest_artworks': Artwork.objects.all().order_by('-created_at')[:3],  # Fetch latest 3 artworks
        'guides': guides,  # Add guides to the context
    }
    
    # Render the index.html template with the merged context
    return render(request, 'home/index.html', context)


def role_selection(request):
    logger.info(f"Role selection page accessed with request: {request}")
    if request.method == 'POST':
        role = request.POST.get('role')
        logger.info(f"User selected role: {role}")
        if role == 'artist':
            return redirect('artist_auth')
        elif role == 'user':
            return redirect('user_auth')
        else:
            return redirect('home')
    return render(request, 'home/role_selection.html')

def artist_auth(request):
    mode = request.GET.get('mode', 'login')
    logger.info(f"Rendering artist auth page with mode: {mode}, method: {request.method}")

    # Determine the form class
    form_class = LoginForm if mode == 'login' else SignupForm
    form = form_class()

    if request.method == 'POST':
        form = form_class(data=request.POST, request=request if mode == 'login' else None)
        
        if form.is_valid():
            if mode == 'signup':
                try:
                    email = form.cleaned_data.get('email')
                    User = get_user_model()
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "An account with this email already exists. Please log in instead.")
                        logger.info(f"Signup failed: Email {email} already exists")
                        return redirect('artist_auth') + '?mode=login'

                    user = form.save(request)
                    ArtistProfile.objects.get_or_create(user=user)
                    messages.success(request, "Successfully signed up as an artist! Please check your email to verify.")
                    logger.info(f"Artist {user.email} signed up successfully")
                    return redirect('artist_auth') + '?mode=login'
                except Exception as e:
                    messages.error(request, f"Signup failed: {str(e)}")
                    logger.error(f"Artist signup error: {str(e)}")
            
            elif mode == 'login':
                form.login(request)
                logger.info(f"Artist {form.user.email} logged in successfully")
                return redirect('prof:artist_dashboard')
        
        for error in form.errors.values():
            messages.error(request, error[0])
            logger.error(f"Artist auth form error: {error[0]}")

    return render(request, 'prof/artist_auth.html', {'mode': mode, 'form': form})

def user_auth(request):
    mode = request.GET.get('mode', 'login')
    logger.info(f"Rendering user auth page with mode: {mode}")

    form_class = LoginForm if mode == 'login' else SignupForm
    form = form_class()

    if request.method == 'POST':
        form = form_class(data=request.POST, request=request if mode == 'login' else None)

        if form.is_valid():
            if mode == 'signup':
                try:
                    email = form.cleaned_data.get('email')
                    User = get_user_model()
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "An account with this email already exists. Please log in instead.")
                        logger.info(f"Signup failed: Email {email} already exists")
                        return redirect('user_auth') + '?mode=login'

                    user = form.save(request)
                    RegularUserProfile.objects.get_or_create(user=user)
                    messages.success(request, "Successfully signed up! Please check your email to verify.")
                    logger.info(f"User {user.email} signed up successfully")
                    return redirect('user_auth') + '?mode=login'
                except Exception as e:
                    messages.error(request, f"Signup failed: {str(e)}")
                    logger.error(f"User signup error: {str(e)}")

            elif mode == 'login':
                form.login(request)
                logger.info(f"User {form.user.email} logged in successfully")
                return redirect('home')

        for error in form.errors.values():
            messages.error(request, error[0])
            logger.error(f"User auth form error: {error[0]}")

    return render(request, 'home/user_auth.html', {'mode': mode, 'form': form})

@login_required
@user_passes_test(is_normal_user)
def user_profile(request):
    user_profile, created = RegularUserProfile.objects.get_or_create(user=request.user)
    return render(request, 'home/user_profile.html', {'user_profile': user_profile})

@login_required
@user_passes_test(is_normal_user)
def buy_art(request):
    artworks = Artwork.objects.filter(is_available=True)
    return render(request, 'home/buy_art.html', {'artworks': artworks})

@login_required
@user_passes_test(is_normal_user)
def booking(request):
    return render(request, 'home/booking.html')

def about_us(request):
    return render(request, 'home/about_us.html', {
        'is_artist': is_artist(request.user),
        'is_normal_user': is_normal_user(request.user),
    })

# def destinations(request):
#     destinations = Destination.objects.all()
#     return render(request, 'home/destinations.html', {'destinations': destinations})

# def destination_detail(request, destination_id):
#     destination = get_object_or_404(Destination, id=destination_id)
#     return render(request, 'home/destination_detail.html', {'destination': destination})

def tours(request):
    return render(request, 'home/tours.html')

def travel_guides(request):
    return render(request, 'home/travel_guides.html')

def special_offers(request):
    return render(request, 'home/special_offers.html')

def blog(request):
    return render(request, 'home/blog.html')

def book_now(request):
    return render(request, 'home/book_now.html')

def gallery(request):
    artworks = Artwork.objects.all()  # Fetch all artworks
    return render(request, 'home/gallery.html', {'artworks': artworks})
