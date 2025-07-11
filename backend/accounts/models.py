from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser # for AbstracUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin # for AbstractBaseUser

# Create your models here.

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'), # Can access everything
        ('manager', 'Manager'), # Can manage employees, has some restrictions to certain admin features
        ('employee', 'Employee'), # Limited access, has full access to books
    ]

    username = None
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        return super().save(*args, **kwargs)
    

# class CustomAddress(models.Model):
#     pass
    

# # NOT USED, for learning purposes only
# class unused_CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField("email address", unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email