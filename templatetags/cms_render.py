from django import template
from django.utils.safestring import mark_safe

register = template.Library()


class RenderNode(template.Node):
	def __init__(self, content):
		self.content = content

	def render(self, context):
		try:
			self.content = template.resolve_variable(self.content, context)
			return template.Template(self.content).render(template.Context(context, autoescape=False))
		except template.TemplateSyntaxError, e:
			return mark_safe("<strong>Template error: There is an error one of this page's template tags: <code>%s</code></small>" % e.message)


@register.tag(name='cms_render')
def cms_render(parser, token):
	"""
	Example: {% cms_render flatpage.content %}
	"""
	content = token.split_contents()[-1]
	return RenderNode(content)
cms_render.is_safe = True
