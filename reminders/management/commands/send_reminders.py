from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from reminders.models import Reminder
from vehicles.models import Vehicle
from users.models import CustomUser
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send reminder emails to users whose vehicle registrations are nearing expiry.'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        reminders_sent = 0
        vehicles = Vehicle.objects.select_related('user')

        for vehicle in vehicles:
            try:
                user = vehicle.user
                if not user.email:
                    logger.warning(f"User {user.username} has no email. Skipping.")
                    continue

                reminder_days = user.reminder_days_before or 7
                reminder_date = vehicle.expiry_date - timedelta(days=reminder_days)

                if reminder_date != today or not user.notify_by_email:
                    continue

                # Avoid duplicate reminders
                reminder_exists = Reminder.objects.filter(
                    user=user,
                    vehicle=vehicle,
                    reminder_date=reminder_date,
                    status='sent'
                ).exists()

                if reminder_exists:
                    logger.info(f"Reminder already sent for {vehicle.plate_number} on {reminder_date}.")
                    continue

                subject = f"Reminder: Vehicle {vehicle.plate_number} Expiring Soon"
                message = (
                    f"Hello {user.username},\n\n"
                    f"Your vehicle '{vehicle.vehicle_name}' with plate number {vehicle.plate_number} "
                    f"is set to expire on {vehicle.expiry_date}.\n\n"
                    f"Please take action to renew it.\n\n"
                    "Best regards,\nVehicle Reminder System"
                )

                try:
                    send_mail(
                        subject,
                        message,
                        'noreply@vehiclereminder.com',
                        [user.email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    logger.error(f"Invalid header when sending to {user.email}")
                    continue
                except Exception as e:
                    logger.exception(f"Failed to send email to {user.email}: {str(e)}")
                    continue

                try:
                    Reminder.objects.create(
                        user=user,
                        vehicle=vehicle,
                        reminder_date=reminder_date,
                        status='sent'
                    )
                except Exception as e:
                    logger.exception(f"Failed to save reminder for {user.username}: {str(e)}")
                    continue

                reminders_sent += 1
                self.stdout.write(f"Reminder sent to {user.email} for vehicle {vehicle.plate_number}")

            except Exception as e:
                logger.exception(f"Unexpected error processing vehicle ID {vehicle.id}: {str(e)}")
                continue

        self.stdout.write(self.style.SUCCESS(f"Finished: {reminders_sent} reminder(s) sent."))
