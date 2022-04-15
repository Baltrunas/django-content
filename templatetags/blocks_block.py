# -*- utf-8 -*-
# import and register template library
from django import template
register = template.Library()

# import models
from ..models import Block
# import regex
import re


@register.simple_tag(takes_context=True)
def blocks_block(context, slug):
	request = context['request']

	context['block'] = False

	blocks = Block.objects.filter(public=True, sites__in=[request.site], slug=slug)
	for block in blocks:
		for block_url in block.urls.all():
			if block_url.regex:
				url_re = re.compile(block_url.url)
				if url_re.findall(request.url):
					context['block'] = block
			else:
				if block_url.url == request.url:
					context['block'] = block

	tpl = template.loader.get_template('blocks/block.html')
	return tpl.render(template.Context(context))
