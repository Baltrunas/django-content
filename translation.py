from django.contrib import admin

from modeltranslation.translator import register, TranslationOptions
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Page, Block, Element
from .admin import PageAdmin


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ["title", "header", "keywords", "description", "intro", "text", "image"]


@register(Block)
class BlockTranslationOptions(TranslationOptions):
    fields = ["header", "description", "text", "image"]


@register(Element)
class ElementTranslationOptions(TranslationOptions):
    fields = ["header", "description", "text", "image"]


admin.site.unregister(Page)


@admin.register(Page)
class PageAdmin(PageAdmin, TabbedTranslationAdmin):
    pass
