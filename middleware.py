from django.http import Http404
from django.conf import settings

from .models import Page
from .views import page


class PageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code != 404:
            return response

        try:
            return page(request, request.path_info)
        except Http404:
            return response
        except Exception as e:
            if settings.DEBUG:
                raise e
            return response

    def process_template_response(self, request, response):
        pages_list = Page.objects.filter(public=True, url=request.path_info, sites__in=[request.site])
        if pages_list.count() == 1 and pages_list[0].template:
            response.template_name = pages_list[0].template
        return response
