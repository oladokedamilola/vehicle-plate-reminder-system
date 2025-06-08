from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CustomLoginForm
from vehicles.models import Vehicle
from django.contrib import messages
from reminders.models import *
from datetime import date, timedelta
from django.utils.timezone import localtime
from django.utils import timezone

User = get_user_model()

def register_view(request):
    if request.user is authenticate:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user is authenticate:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def dashboard(request):
    user = request.user

    # Get vehicles owned by the logged-in user
    vehicles = Vehicle.objects.filter(user=user).order_by('-created_at')
    current_hour = localtime().hour  # get current hour in local time
    # Calculate vehicle stats
    total_vehicles = vehicles.count()
    expiring_soon = vehicles.filter(expiry_date__range=[timezone.now(), timezone.now() + timedelta(days=30)]).count()
    expired = vehicles.filter(expiry_date__lt=timezone.now()).count()
    reminders_sent = Reminder.objects.filter(user=user, status = "sent").count()


    # Pass user details to the context explicitly (optional, for clarity)
    context = {
        'total_vehicles': total_vehicles,
        'expiring_soon': expiring_soon,
        'expired': expired,
        'reminders_sent': reminders_sent,
        'current_hour': current_hour,
        'user': user,  # Not strictly necessary, but explicit in case of template extension conflicts
    }

    return render(request, 'users/dashboard.html', context)




from .forms import UserProfileForm

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile details updated!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'users/update_profile.html', {'form': form})





from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import NotificationSettingsForm

@login_required
def update_settings(request):
    user = request.user

    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your settings have been updated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NotificationSettingsForm(instance=user)

    return render(request, 'users/settings.html', {'form': form})


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
@require_POST
def mark_notification_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)




@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/user_notifications.html', {'notifications': notifications})
