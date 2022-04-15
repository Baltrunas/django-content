# -*- utf-8 -*-
from django.template import Context
from django.template import Template

from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def render(context, content):
	try:
		tpl = Template(content)
		content = Context(context)
		return tpl.render(content)
	except:
		return 'Render Error'
