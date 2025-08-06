from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Page, Region, District


@admin.register(Page)
class PageAdmin(TranslationAdmin):
    list_display = ('slug', 'title')


@admin.register(Region)
class RegionAdmin(TranslationAdmin):
    list_display = ("id", "name")


@admin.register(District)
class DistrictAdmin(TranslationAdmin):
    list_display = ("id", "name", "region")
    list_filter = ("region",)