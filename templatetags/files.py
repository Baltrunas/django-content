from django.contrib.contenttypes.models import ContentType

from django import template
register = template.Library()

from ..models import File


@register.simple_tag(takes_context=True)
def files(context, files_object, group, tpl='files/thumbnail.html', size=''):
	context['size'] = size
	content_type = ContentType.objects.get_for_model(type(files_object))
	object_id = files_object.id
	context['files'] = File.objects.filter(content_type=content_type, object_id=object_id, group=group, public=True)

	tpl = template.loader.get_template(tpl)
	return tpl.render(template.Context(context))
