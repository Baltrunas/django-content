from django.contrib import admin
from feincms3.admin import TreeAdmin

from .models import Page


@admin.register(Page)
class PageAdmin(TreeAdmin):
    list_display = ["indented_title", "move_column", "slug", "url", "position", "public"]
    search_fields = ["name", "slug", "id"]
    list_editable = ["public"]
    list_filter = ["public", "sites"]
