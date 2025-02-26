from django.urls import path
from accounts.views import *
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    #User view urls with login, register, logout, and email activation.
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
]