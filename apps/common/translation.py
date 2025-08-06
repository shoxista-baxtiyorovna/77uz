from modeltranslation.translator import TranslationOptions, register

from .models import District, Page, Region


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ("name",)
