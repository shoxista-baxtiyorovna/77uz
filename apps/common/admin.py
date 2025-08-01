from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Page

@admin.register(Page)
class PageAdmin(TranslationAdmin):
    list_display = ('slug', 'title')