from projman.models import Task
from django import template

register = template.Library()

@register.inclusion_tag('show_tasks.html')
def show_tasks(project, complete=0):
	tasks = Task.objects.filter(project=project.id, complete=complete).order_by('-completed' if complete else 'priority')

	if complete:
		tasks = tasks[:5]

	return locals()


@register.inclusion_tag('show_history.html')
def show_history(category):
	tasks = Task.objects.filter(project__category__exact=category).filter(complete=1).order_by('-completed')[:15]
	
	return locals()
	

@register.simple_tag
def active(request, pattern):
	import re
	if re.search(pattern, request.path):
		return 'active'
	return ''