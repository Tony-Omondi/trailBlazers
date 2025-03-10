from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('prof/', include('prof.urls', namespace='prof')),  # Maps /prof/ to prof app
    path('', include('home.urls')),  # Keep home app untouched
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)