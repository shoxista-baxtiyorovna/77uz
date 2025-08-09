from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from modeltranslation.admin import TranslationAdmin

from .models import Address, CustomUser


@admin.register(Address)
class AddressAdmin(TranslationAdmin):
    list_display = ("id", "name", "lat", "long")
    search_fields = ("name",)


@admin.register(CustomUser)
class CustomUserAdmin(TranslationAdmin, BaseUserAdmin):
    ordering = ("id",)
    list_display = ("id", "full_name", "phone_number", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("full_name", "phone_number")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Shaxsiy ma'lumotlar", {"fields": ("full_name", "profile_photo", "address")}),
        ("Rollar va huquqlar", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Tizim ma'lumotlari", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "full_name",
                    "password1",
                    "password2",
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
