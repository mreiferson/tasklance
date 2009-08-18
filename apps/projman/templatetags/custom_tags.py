from projman.models import Todo
from django import template

register = template.Library()

@register.inclusion_tag('show_todos.html')
def show_todos(category, complete=0):
	todos = Todo.objects.filter(category=category.id, complete=complete).order_by('-completed' if complete else 'priority')

	if complete:
		todos = todos[:5]

	return locals()


@register.inclusion_tag('show_history.html')
def show_history(project):
	todos = Todo.objects.filter(category__project__exact=project).filter(complete=1).order_by('-completed')[:15]
	
	return locals()