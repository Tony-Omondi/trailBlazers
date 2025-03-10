from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


app_name = 'prof'

urlpatterns = [
    path('artist-dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('upload/', views.upload_artwork, name='upload_artwork'),
    path('profile/edit/', views.edit_artist_profile, name='edit_artist_profile'),
    path('auth/', views.artist_auth, name='artist_auth'),  # Added auth endpoint
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)