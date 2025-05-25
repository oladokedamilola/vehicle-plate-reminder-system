from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def plate_image_upload_path(instance, filename):
    return f'vehicles/vehicle_{instance.id}/plate_images/{filename}'


class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=20)
    plate_image = models.ImageField(upload_to=plate_image_upload_path, blank=True, null=True)
    registration_date = models.DateField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'vehicle_name'], name='unique_vehicle_name_per_user'),
            models.UniqueConstraint(fields=['user', 'model'], name='unique_model_per_user'),
            models.UniqueConstraint(fields=['user', 'plate_number'], name='unique_plate_per_user'),
        ]

    def save(self, *args, **kwargs):
        self.plate_number = self.plate_number.upper().strip()
        self.vehicle_name = self.vehicle_name.upper().strip()
        self.model = self.model.upper().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plate_number} ({self.vehicle_name})"
