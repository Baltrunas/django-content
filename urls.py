from django.urls import re_path
from .views import PageView


urlpatterns = [
    re_path(r"^api/page(?P<url>.*)$", PageView.as_view(), name="api_page"),
]
