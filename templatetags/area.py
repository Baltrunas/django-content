import re
from django import template

# from ..models import URL
from ..models import Area, Block


register = template.Library()


@register.simple_tag(takes_context=True)
def area(context, slug):
    request = context["request"]
    context["area"] = Area.objects.get(slug=slug)

    # TODO: get all blocks
    try:
        for url in URL.objects.all():
            if url.regex:
                url_re = re.compile(url.url)
                if url_re.findall(request.url):
                    regex_urls_blocks = Block.objects.filter(public=True, sites=request.site, urls=url, area=area)
                    blocks_area += regex_urls_blocks
            else:
                plain_urls_blocks = Block.objects.filter(
                    public=True, sites=request.site, urls__url=request.url, area=area
                )
                blocks_area += plain_urls_blocks
        blocks_area_ids = [block.id for block in list(set(blocks_area))]
        blocks_area = Block.objects.filter(pk__in=blocks_area_ids).order_by("order")
    except:
        pass

    context["area"] = area
    context["blocks"] = blocks

    tpl = template.loader.get_template("content/area.html")
    return tpl.render(template.Context(context))
