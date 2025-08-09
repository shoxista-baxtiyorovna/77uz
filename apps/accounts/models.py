from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


class Address(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        SUPER_ADMIN = "super_admin", "Super Admin"
        SELLER = "seller", "Seller"

    class Status(models.TextChoices):
        PENDING = "pending", "Kutilmoqda"
        ACTIVE = "active", "Faol"
        REJECTED = "rejected", "Rad etilgan"

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    address = models.OneToOneField(
        Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="user"
    )
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.SELLER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.role} - {self.status})"
