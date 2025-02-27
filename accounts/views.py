import os
import uuid
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.template.loader import get_template
from accounts.models import Profile
from base.emails import send_account_activation_email
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect, render, get_object_or_404
from accounts.forms import UserUpdateForm, UserProfileForm, CustomPasswordChangeForm


# ✅ LOGIN VIEW
def login_page(request):
    next_url = request.GET.get('next')  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()

        if not user_obj:
            messages.warning(request, 'Account not found!')
            return HttpResponseRedirect(request.path_info)

        # ✅ Ensure Profile Exists (Fix the RelatedObjectDoesNotExist error)
        profile, created = Profile.objects.get_or_create(user=user_obj)

        if not profile.is_email_verified:
            messages.error(request, 'Account not verified! Please check your email.')
            return HttpResponseRedirect(request.path_info)

        # ✅ Authenticate user
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(request, user_obj)
            messages.success(request, 'Login successful.')

            # ✅ Check if the next URL is safe
            if url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('index')

        messages.warning(request, 'Invalid credentials.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')



# ✅ REGISTER VIEW (Fixed Profile Creation Issue)
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ✅ Check if user already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.info(request, 'Username or email already exists!')
            return HttpResponseRedirect(request.path_info)

        # ✅ Create User
        user_obj = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, email=email, password=password
        )

        # ✅ Ensure Profile is created
        profile, created = Profile.objects.get_or_create(user=user_obj)
        profile.email_token = str(uuid.uuid4())
        profile.save()

        # ✅ Send account activation email
        send_account_activation_email(email, profile.email_token)
        messages.success(request, "An email has been sent for verification.")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


# ✅ LOGOUT VIEW
@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, "Logged out successfully!")
    return redirect('index')


# ✅ ACCOUNT ACTIVATION VIEW
def activate_email_account(request, email_token):
    try:
        profile = Profile.objects.get(email_token=email_token)
        profile.is_email_verified = True
        profile.save()
        messages.success(request, 'Account verification successful. You can now log in.')
        return redirect('login')
    except Profile.DoesNotExist:
        return HttpResponse('Invalid or expired email token.', status=400)


# ✅ PROFILE VIEW
@login_required
def profile_view(request, username):
    user_name = get_object_or_404(User, username=username)
    user = request.user
    profile = user.profile

    user_form = UserUpdateForm(instance=user)
    profile_form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'user_name': user_name,
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'accounts/profile.html', context)


# ✅ CHANGE PASSWORD VIEW
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Password updated successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
