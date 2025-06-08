from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from vehicles.models import Vehicle
from reminders.models import Reminder
from users.models import *


@receiver(post_save, sender=Vehicle)
def notify_new_vehicle_reminder(sender, instance, created, **kwargs):
    if created:
        message = (
            f"A new reminder has been created for your vehicle '{instance.vehicle_name}' "
            f"expiring on {instance.expiry_date}."
        )

        # Send email if user has opted in
        if instance.user.notify_by_email:
            send_mail(
                "New Reminder Created",
                f"Hello {instance.user.username},\n\n{message}\n\nThank you.",
                'noreply@yourdomain.com',
                [instance.user.email]
            )

        # Save notification to DB
        Notification.objects.create(
            user=instance.user,
            type='vehicle',
            message=message
        )

@receiver(post_save, sender=CustomUser)
def notify_user_pref_change(sender, instance, **kwargs):
    message = "Your reminder notification preferences have been updated."

    # Send email if user has opted in
    if instance.notify_by_email:
        send_mail(
            "Notification Preferences Updated",
            f"Hello {instance.username},\n\n{message}\n\nThank you.",
            'noreply@yourdomain.com',
            [instance.email]
        )

    # Save notification to DB
    Notification.objects.create(
        user=instance,
        type='settings',
        message=message
    )
