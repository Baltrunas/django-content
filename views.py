from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PageSerializer
from .models import Page


@csrf_protect
def page(request, url):
    context = dict()
    content_page = get_object_or_404(Page, url=url, sites__in=[request.site])

    # Pagination
    current_page_number = request.GET.get("page", 1)
    paginator = Paginator(content_page.children.filter(public=True, sites__in=[request.site]), content_page.per_page)
    try:
        page_children_list = paginator.page(current_page_number)
    except PageNotAnInteger:
        page_children_list = paginator.page(1)
    except EmptyPage:
        page_children_list = paginator.page(paginator.num_pages)

    # Template
    if content_page.template:
        template = content_page.template
    else:
        template = "content/page.html"

    context["page"] = content_page
    context["page_children_list"] = page_children_list
    return render(request, template, context)


class PageView(APIView):
    """
    API Page view endpoint.
    """

    permission_classes = [permissions.AllowAny]

    def get_object(self, url):
        return get_object_or_404(Page, url=url, sites__in=[self.request.site])

    def get(self, request, url, format=None):
        serializer = PageSerializer(self.get_object(url), context={"request": self.request})
        return Response(serializer.data)
