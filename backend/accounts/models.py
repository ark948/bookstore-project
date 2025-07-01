from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    pass