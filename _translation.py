from django.contrib import admin

from modeltranslation.translator import register, TranslationOptions
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Tag, Page, Block, Element, Media
from .admin import PageAdmin


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ["title", "header", "keywords", "description", "intro", "text"]


@register(Block)
class BlockTranslationOptions(TranslationOptions):
    fields = ["title", "description", "text", "url"]


@register(Element)
class ElementTranslationOptions(TranslationOptions):
    fields = ["title", "description", "text"]


@register(Media)
class MediaTranslationOptions(TranslationOptions):
    fields = ["name", "description", "doc"]


admin.site.unregister(Page)


@admin.register(Page)
class PageAdmin(PageAdmin, TabbedTranslationAdmin):
    pass
