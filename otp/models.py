import uuid
import random
import string
from django.db import models
from django.utils import timezone

class OTPTransaction(models.Model):
    mobile_no = models.CharField(max_length=10, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    otp = models.CharField(max_length=6, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.transaction_id} to {self.destination_number}"
