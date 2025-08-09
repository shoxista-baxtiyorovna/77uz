from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Foydalanuvchida telefon raqami bo‘lishi shart")

        user = self.model(phone_number=phone_number, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", self.model.Roles.SUPER_ADMIN)
        extra_fields.setdefault("status", self.model.Status.ACTIVE)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser uchun is_staff=True bo‘lishi shart")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser uchun is_superuser=True bo‘lishi shart")

        return self.create_user(phone_number, full_name, password, **extra_fields)
