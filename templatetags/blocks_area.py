# import and register template library
from django import template
register = template.Library()

# import models
from ..models import Block
from ..models import URL
# import regex
import re


@register.simple_tag(takes_context=True)
def blocks_area(context, area):
	request = context['request']

	blocks_area = []

	try:
		for url in URL.objects.all():
			if url.regex:
				url_re = re.compile(url.url)
				if url_re.findall(request.url):
					regex_urls_blocks = Block.objects.filter(public=True, sites=request.site, urls=url, area=area)
					blocks_area += regex_urls_blocks
			else:
				plain_urls_blocks = Block.objects.filter(public=True, sites=request.site, urls__url=request.url, area=area)
				blocks_area += plain_urls_blocks
		blocks_area_ids = [block.id for block in list(set(blocks_area))]
		blocks_area = Block.objects.filter(pk__in=blocks_area_ids).order_by('order')
	except:
		pass

	context['area'] = area
	context['blocks_area'] = blocks_area

	tpl = template.loader.get_template('blocks/area.html')
	return tpl.render(template.Context(context))
