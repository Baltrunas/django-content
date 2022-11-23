from .models import Page


def page(request):
    return {
        "page": Page.objects.filter(public=True, url=request.path_info, sites__in=[request.site]).first(),
    }
