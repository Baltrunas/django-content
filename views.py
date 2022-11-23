from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

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
