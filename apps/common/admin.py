from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import District, Page, Region, Setting


@admin.register(Page)
class PageAdmin(TabbedTranslationAdmin):
    list_display = ("id", "slug", "title")


@admin.register(Region)
class RegionAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name")


@admin.register(District)
class DistrictAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "region")
    list_filter = ("region",)


@admin.register(Setting)
class SettingAdmin(TabbedTranslationAdmin):
    list_display = ("id", "phone", "maintenance_mode")
