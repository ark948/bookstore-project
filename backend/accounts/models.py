from django.db import models
from django.contrib.auth.models import AbstractUser # for AbstracUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin # for AbstractBaseUser

from encrypted_fields.fields import EncryptedTextField, EncryptedIntegerField, EncryptedEmailField

# Create your models here.

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'), # Can access everything
        ('manager', 'Manager'), # Can manage employees, has some restrictions to certain admin features
        ('employee', 'Employee'), # Limited access, has full access to books
        ('user', 'User') # aka customers
    ]

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=60, blank=True)

    username = None
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        return super().save(*args, **kwargs)
    


class UserProfile(models.Model):
    user = models.OneToOneField(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile"
    )

    postal_code = EncryptedIntegerField("Postal Code", null=True, blank=True)
    province = models.OneToOneField("accounts.Province", on_delete=models.SET_NULL, null=True, blank=True)
    city = models.OneToOneField("accounts.City", on_delete=models.SET_NULL, null=True, blank=True)
    landline = EncryptedIntegerField("Landline", null=True, blank=True)
    address = EncryptedTextField("Address", max_length=500, null=True)


    def __str__(self) -> str:
        return f"{self.user}"
    
    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "user_profiles"


class Province(models.Model):
    name = models.CharField(max_length=100);

    def __str__(self):
        return self.name
    

class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


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