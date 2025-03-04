from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.profile_view, name='prof'),
    path('upload/', views.upload_artwork, name='upload_artwork'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)