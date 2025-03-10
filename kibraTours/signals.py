from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def custom_login_redirect(request, user, **kwargs):
    logger.info(f"User {user.email} logged in, redirecting to artist dashboard")
    return reverse('prof:artist_dashboard')