from django.contrib.auth.models import AbstractUser
from django.db import models

import os
from django.utils.text import get_valid_filename

def profile_picture_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    base = get_valid_filename(base)[:90]  # limit base to 90 chars
    return f'profile_pics/{base}{ext}'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    notify_by_email = models.BooleanField(default=True)
    notify_by_sms = models.BooleanField(default=False)
    reminder_days_before = models.IntegerField(default=7)  # e.g., remind 7 days before expiry

    bio = models.TextField(max_length=300, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, blank=True, null=True)

    def __str__(self):
        return self.username




