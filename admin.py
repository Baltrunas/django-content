from django.contrib import admin
from django.utils.translation import gettext as _
from django import forms
from django.db import models

from feincms3.admin import TreeAdmin

from .models import Page, Area, Block, Element


@admin.register(Page)
class PageAdmin(TreeAdmin):
    list_display = ["indented_title", "move_column", "slug", "url", "position", "public"]
    search_fields = ["name", "title", "header", "slug", "id"]
    list_editable = ["public"]
    list_filter = ["public", "sites", "parent"]
    fieldsets = (
        (None, {"fields": ("name",)}),
        (
            _("SEO"),
            {"classes": ("collapse",), "fields": ("title", "keywords", "description", "head_code", "footer_code")},
        ),
        (_("Content"), {"fields": ("header", "intro", "text", "image",)}),
        (_("Settings"), {"fields": ("slug", "sites", "position",)}),
        (_("Template"), {"classes": ("collapse",), "fields": ("template", "per_page",)}),
        (None, {"fields": ("public",)}),
    )
    formfield_overrides = {
        models.CharField: {"widget": forms.TextInput(attrs={"size": 95})},
        models.TextField: {"widget": forms.Textarea(attrs={"rows": 10, "cols": 95})},
    }
    save_as = True


class ElementInline(admin.StackedInline):
    model = Element
    verbose_name = _("Element")
    verbose_name_plural = _("Elements")
    extra = 0


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "public"]
    search_fields = ["name", "slug", "public"]
    list_filter = ["public"]
    list_editable = ["public"]


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "position", "public"]
    search_fields = ["name", "header", "slug"]
    list_filter = ["public", "area", "pages"]
    list_editable = ["public", "position"]
    inlines = [ElementInline]
    save_as = True


admin.site.register(Element)
