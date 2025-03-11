import requests
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from allauth.account.forms import LoginForm, SignupForm
from allauth.account.utils import get_user_model
from .models import ArtistProfile, Artwork, Order
from .forms import ArtistProfileForm, ArtworkForm, OrderForm
import logging

logger = logging.getLogger(__name__)

# Pesapal Configuration
APP_ENVIRONMENT = 'live'  # or 'sandbox'
consumer_key = "3uOP67/JqieNDq7lJzpKgJr0j0AsnHFr"
consumer_secret = "GwdOVSKze2Mpx1oVYeLH4cbxDRo="

if APP_ENVIRONMENT == 'sandbox':
    api_url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
    ipn_registration_url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"
    submit_order_url = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"
else:
    api_url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"
    ipn_registration_url = "https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN"
    submit_order_url = "https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest"

def request_token():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret
    }
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        logger.error(f"Error requesting token: {response.status_code}")
        return None

def register_ipn(token):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "url": "https://your-ngrok-url.ngrok-free.app/prof/pesapal-ipn/",  # Replace with your IPN URL
        "ipn_notification_type": "POST"
    }
    response = requests.post(ipn_registration_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('ipn_id')
    else:
        logger.error(f"Error registering IPN: {response.status_code}")
        return None

def submit_order(token, ipn_id, artwork, buyer_details):
    merchant_reference = random.randint(1, 1000000000000000000)
    amount = artwork.price
    callback_url = f"http://127.0.0.1:8000/prof/payment-success/?merchant_reference={merchant_reference}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "id": str(merchant_reference),
        "currency": "KES",
        "amount": float(amount),
        "description": f"Payment for artwork: {artwork.title}",
        "callback_url": callback_url,
        "notification_id": ipn_id,
        "branch": "KibraConnect",
        "billing_address": {
            "email_address": buyer_details['email'],
            "phone_number": buyer_details['phone'],
            "country_code": "KE",
            "first_name": buyer_details['name'].split()[0] if buyer_details['name'].split() else "",
            "middle_name": "",
            "last_name": buyer_details['name'].split()[-1] if buyer_details['name'].split() else "",
            "line_1": "KibraConnect Customer",
            "line_2": "",
            "city": "",
            "state": "",
            "postal_code": "",
            "zip_code": ""
        }
    }

    response = requests.post(submit_order_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json(), merchant_reference
    else:
        logger.error(f"Error submitting order: {response.status_code}")
        return None, None

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
                    return redirect('prof:artist_auth?mode=login')
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
        form = form_class()

    return render(request, 'prof/artist_auth.html', {'mode': mode, 'form': form})

def buy_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id, is_available=True)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            buyer_details = {
                'name': form.cleaned_data['buyer_name'],
                'email': form.cleaned_data['buyer_email'],
                'phone': form.cleaned_data['buyer_phone']
            }
            # Step 1: Get token
            token = request_token()
            if not token:
                messages.error(request, "Failed to initiate payment. Please try again.")
                return redirect('prof:buy_artwork', artwork_id=artwork.id)

            # Step 2: Register IPN
            ipn_id = register_ipn(token)
            if not ipn_id:
                messages.error(request, "Failed to set up payment notifications. Please try again.")
                return redirect('prof:buy_artwork', artwork_id=artwork.id)

            # Step 3: Submit order
            order_response, merchant_reference = submit_order(token, ipn_id, artwork, buyer_details)
            if order_response and order_response.get('status') == "200":
                # Create a pending order
                order = Order.objects.create(
                    buyer=request.user,
                    artwork=artwork,
                    transaction_id=order_response.get('order_tracking_id'),
                    buyer_name=buyer_details['name'],
                    buyer_email=buyer_details['email'],
                    buyer_phone=buyer_details['phone'],
                    artist=artwork.artist,
                    amount=artwork.price,
                    is_completed=False
                )
                return render(request, 'prof/payment_iframe.html', {
                    'redirect_url': order_response.get('redirect_url'),
                    'order': order
                })
            else:
                messages.error(request, "Failed to process payment. Please try again.")
                return redirect('prof:buy_artwork', artwork_id=artwork.id)
    else:
        form = OrderForm()
    return render(request, 'prof/buy_artwork.html', {'form': form, 'artwork': artwork})

def payment_success(request):
    merchant_reference = request.GET.get('merchant_reference')
    order = get_object_or_404(Order, transaction_id=merchant_reference)
    order.is_completed = True
    order.artwork.is_available = False  # Mark artwork as sold
    order.artwork.save()
    order.save()  # This triggers email notifications
    return render(request, 'prof/payment_success.html', {'order': order})

def pesapal_ipn(request):
    if request.method == 'POST':
        data = request.POST
        order_tracking_id = data.get('OrderTrackingId')
        order = Order.objects.filter(transaction_id=order_tracking_id).first()
        if order:
            order.is_completed = True
            order.artwork.is_available = False
            order.artwork.save()
            order.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "order not found"}, status=404)
    return JsonResponse({"status": "invalid request"}, status=400)