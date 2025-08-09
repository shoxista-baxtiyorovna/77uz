from modeltranslation.translator import TranslationOptions, register

from .models import Address, CustomUser


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    fields = ("full_name",)
