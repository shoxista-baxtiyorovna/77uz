from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Ad, AdImage, Category


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "parent")
    search_fields = ("parent",)


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1
    fields = ("image", "is_main", "created_time")
    readonly_fields = ["created_time"]
    show_change_link = True


@admin.register(Ad)
class AdAdmin(TabbedTranslationAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "category",
        "description",
        "price",
        "status",
        "view_count",
    )
    list_filter = ("status", "category")
    search_fields = ("name", "slug", "description")
    ordering = ("-created_time",)
    inlines = [AdImageInline]
