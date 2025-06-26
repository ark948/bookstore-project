from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=14, unique=True, blank=True, null=True, validators=[
        RegexValidator(regex=r"^\d{11}", message="شماره همراه می‌بایست 11 رقمی باشد.")
    ])
    address = models.TextField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(unique=True)