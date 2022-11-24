from rest_framework import serializers

from .models import Page


class PageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Page
        fields = [
            "id",
            "name",
            "title",
            "header",
            "keywords",
            "description",
            "head_code",
            "footer_code",
            "image",
            "intro",
            "text",
            "sites",
            "slug",
            "url",
            "template",
            "per_page",
            "position",
            "public",
            "created_at",
            "updated_at",
        ]
