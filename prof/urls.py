from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prof'

urlpatterns = [
    path('artist-dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('upload/', views.upload_artwork, name='upload_artwork'),
    path('profile/edit/', views.edit_artist_profile, name='edit_artist_profile'),
    path('auth/', views.artist_auth, name='artist_auth'),
    path('buy/<int:artwork_id>/', views.buy_artwork, name='buy_artwork'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('pesapal-ipn/', views.pesapal_ipn, name='pesapal_ipn'),
    path('buyer-signup/', views.BuyerSignupView.as_view(), name='buyer_signup'),
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)