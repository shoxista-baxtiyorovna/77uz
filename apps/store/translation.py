from modeltranslation.translator import TranslationOptions, register

from .models import Ad, Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Ad)
class AdTranslationOptions(TranslationOptions):
    fields = ("name", "description")
