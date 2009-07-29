from projman.models import Todo
from django import template

register = template.Library()

@register.inclusion_tag('show_todos.html')
def show_todos(category, complete=0):
	todos = Todo.objects.filter(category=category.id, complete=complete).order_by(complete and 'completed' or 'priority')
	return { 'todos': todos, 'complete': complete }