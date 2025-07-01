from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser # for AbstracUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin # for AbstractBaseUser

# Create your models here.

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"UserObj {self.pk}"
    

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