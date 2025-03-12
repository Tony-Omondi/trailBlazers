from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# tours/urls.py
from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('', views.destinations, name='destinations'),  # /tours/ maps to destinations
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('booking-success/', views.booking_success, name='booking_success'),  # Add this
    path('pesapal-ipn/', views.pesapal_ipn, name='pesapal_ipn'),  # For IPN
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)