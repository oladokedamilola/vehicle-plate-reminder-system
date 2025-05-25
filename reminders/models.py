from django.db import models
from vehicles.models import Vehicle
from django.contrib.auth import get_user_model


User = get_user_model()


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    reminder_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('sent', 'Sent')], default='pending')

    def __str__(self):
        return f"{self.vehicle.plate_number} - {self.reminder_date} - {self.status}"
