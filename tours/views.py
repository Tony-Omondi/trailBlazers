# tours/views.py
import requests
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Tour, TimeSlot, Booking
from .forms import BookingForm
import logging

logger = logging.getLogger(__name__)

# Pesapal Configuration
APP_ENVIRONMENT = 'live'  # Changed to 'live' to match prof/views.py
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
    logger.info(f"Request token response: {response.status_code} - {response.text}")
    if response.status_code == 200:
        return response.json().get('token')
    logger.error(f"Error requesting token: {response.status_code} - {response.text}")
    return None

def register_ipn(token):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "url": "https://your-ngrok-url.ngrok-free.app/tours/pesapal-ipn/",  # Replace with your ngrok URL
        "ipn_notification_type": "POST"
    }
    response = requests.post(ipn_registration_url, headers=headers, json=data)
    logger.info(f"Register IPN response: {response.status_code} - {response.text}")
    if response.status_code == 200:
        return response.json().get('ipn_id')
    logger.error(f"Error registering IPN: {response.status_code} - {response.text}")
    return None

def submit_order(token, ipn_id, tour, booking_details):
    merchant_reference = str(random.randint(1, 1000000000000000000))
    amount = tour.price
    callback_url = f"http://127.0.0.1:8000/tours/booking-success/?merchant_reference={merchant_reference}"  # Localhost for testing
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "id": merchant_reference,
        "currency": "KES",
        "amount": float(amount),
        "description": f"Booking for tour: {tour.name}",
        "callback_url": callback_url,
        "notification_id": ipn_id,
        "branch": "KibraConnect",
        "billing_address": {
            "email_address": booking_details['customer_email'],
            "phone_number": booking_details['customer_phone'],
            "country_code": "KE",
            "first_name": booking_details['customer_name'].split()[0] if booking_details['customer_name'].split() else "",
            "last_name": booking_details['customer_name'].split()[-1] if booking_details['customer_name'].split() else "",
            "line_1": "KibraConnect Customer",
            "line_2": "",
            "city": "",
            "state": "",
            "postal_code": "",
            "zip_code": ""
        }
    }
    response = requests.post(submit_order_url, headers=headers, json=data)
    logger.info(f"Submit order response: {response.status_code} - {response.text}")
    if response.status_code == 200:
        return response.json(), merchant_reference
    logger.error(f"Error submitting order: {response.status_code} - {response.text}")
    return None, None

def home(request):
    featured_tours = Tour.objects.filter(featured_image__isnull=False)[:3]
    context = {'featured_tours': featured_tours}
    return render(request, 'tours/home.html', context)

def destinations(request):
    tours = Tour.objects.all()
    featured_tours = Tour.objects.filter(featured_image__isnull=False)[:3]
    for i, tour in enumerate(tours):
        tour.delay = i * 100
        tour.booking_form = BookingForm(tour=tour)
    context = {'tours': tours, 'featured_tours': featured_tours}
    return render(request, 'tours/destinations.html', context)

def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    logger.info(f"Book tour called for tour_id: {tour_id}, method: {request.method}")
    
    if request.method == 'POST':
        form = BookingForm(request.POST, tour=tour)
        if form.is_valid():
            booking_details = form.cleaned_data
            logger.info(f"Form valid, booking details: {booking_details}")

            # Pesapal integration
            token = request_token()
            if not token:
                messages.error(request, "Failed to initiate payment. Please try again.")
                return redirect('tours:destinations')

            ipn_id = register_ipn(token)
            if not ipn_id:
                messages.error(request, "Failed to set up payment notifications. Please try again.")
                return redirect('tours:destinations')

            order_response, merchant_reference = submit_order(token, ipn_id, tour, booking_details)
            if order_response and order_response.get('status') == "200":  # Match prof/views.py
                order_tracking_id = order_response.get('order_tracking_id')
                booking = Booking.objects.create(
                    tour=tour,
                    time_slot=booking_details['date_time'],
                    group_size=booking_details['group_size'],
                    tour_duration=booking_details['tour_duration'],
                    tour_type=booking_details['tour_type'],
                    meeting_point=booking_details['meeting_point'],
                    customer_name=booking_details['customer_name'],
                    customer_email=booking_details['customer_email'],
                    customer_phone=booking_details['customer_phone'],
                    amount=tour.price,
                    transaction_id=order_tracking_id,
                    merchant_reference=merchant_reference,
                    is_completed=False
                )
                logger.info(f"Booking created: {booking.id}, redirect_url: {order_response.get('redirect_url')}")
                return render(request, 'tours/payment_iframe.html', {
                    'redirect_url': order_response.get('redirect_url'),
                    'booking': booking
                })
            else:
                messages.error(request, "Failed to process payment. Please try again.")
                return redirect('tours:destinations')
        else:
            logger.error(f"Form invalid: {form.errors}")
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = BookingForm(tour=tour)
    
    context = {'tour': tour, 'form': form}
    return render(request, 'tours/destinations.html', context)

def booking_success(request):
    merchant_reference = request.GET.get('merchant_reference')
    if not merchant_reference:
        logger.error("Merchant reference not found in request")
        return redirect('tours:destinations')
    
    logger.info(f"Looking for booking with merchant_reference: {merchant_reference}")
    booking = get_object_or_404(Booking, merchant_reference=merchant_reference)
    booking.is_completed = True
    booking.time_slot.is_booked = True
    booking.time_slot.save()
    booking.save()
    logger.info(f"Booking {booking.id} marked as completed")
    return render(request, 'tours/booking_success.html', {'booking': booking})

def pesapal_ipn(request):
    if request.method == 'POST':
        data = request.POST
        order_tracking_id = data.get('OrderTrackingId')
        logger.info(f"IPN received: {data}")
        booking = Booking.objects.filter(transaction_id=order_tracking_id).first()
        if booking:
            booking.is_completed = True
            booking.time_slot.is_booked = True
            booking.time_slot.save()
            booking.save()
            logger.info(f"IPN updated booking {booking.id}")
            return JsonResponse({"status": "success"})
        logger.error(f"Booking not found for OrderTrackingId: {order_tracking_id}")
        return JsonResponse({"status": "booking not found"}, status=404)
    logger.warning("Invalid IPN request method")
    return JsonResponse({"status": "invalid request"}, status=400)