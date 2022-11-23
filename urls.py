from django.urls import path

from . import views

urlpatterns = [
    # url(r'^tag/(?P<slug>[-_\w]+)/$', views.tag, name='pages_tag'),
    path("dd1/", views.dd, name="dd")
]
