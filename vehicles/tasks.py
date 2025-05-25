from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from vehicles.models import Vehicle
from django.conf import settings

@shared_task
def send_expiry_notifications():
    today = timezone.now().date()
    reminder_date = today + timedelta(days=7)  # Reminder 7 days before expiry

    vehicles = Vehicle.objects.filter(expiry_date=reminder_date)

    for vehicle in vehicles:
        user = vehicle.user

        # Send Email Notification if enabled
        if user.notify_by_email:
            send_mail(
                subject=f'Reminder: Vehicle {vehicle.plate_number} Expiry',
                message=f'Your vehicle {vehicle.plate_number} is expiring on {vehicle.expiry_date}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

        # Send SMS Notification if enabled (Assuming you have an SMS service configured)
        if user.notify_by_sms:
            # You can integrate an SMS API like Twilio here
            pass

    return "Notifications Sent"
