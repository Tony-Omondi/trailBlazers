from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    
    
    path('destinations/', views.destinations, name='destinations'),
    path('destinations/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('tours/', views.tours, name='tours'),
    path('travel_guides/', views.travel_guides, name='travel_guides'),
    path('special_offers/', views.special_offers, name='special_offers'),
    path('blog/', views.blog, name='blog'),
    path('book_now/', views.book_now, name='book_now'),
    path('gallery/', views.gallery, name='gallery'),
    path('auth/artist/', views.artist_auth, name='artist_auth'),
    path('auth/user/', views.user_auth, name='user_auth'),
    path('auth/role-selection/', views.role_selection, name='role_selection'),  # Added
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('user-profile/', views.user_profile, name='user_profile'),path('', views.home, name='home'),
    path('auth/', views.artist_auth, name='artist_auth'),  # Simplified to single auth path
    path('auth/role-selection/', views.role_selection, name='role_selection'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('buy-art/', views.buy_art, name='buy_art'),
    path('booking/', views.booking, name='booking'),
    path('auth/role-selection/', views.role_selection, name='role_selection'),

]