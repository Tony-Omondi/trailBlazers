from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from prof.models import ArtistProfile
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        logger.info(f"Pre-social login for email: {email}")
        if email:
            try:
                user = User.objects.get(email=email)
                logger.info(f"Email {email} exists, connecting to user {user}")
                if not sociallogin.is_existing:
                    sociallogin.connect(request, user)
            except User.DoesNotExist:
                logger.info(f"Email {email} does not exist, proceeding with signup")
                pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        logger.info(f"New user {user.email} created via social login, creating ArtistProfile")
        ArtistProfile.objects.get_or_create(user=user)
        return user