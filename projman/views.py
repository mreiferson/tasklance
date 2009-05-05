from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from forms import *


def overview(request):
	projects = Project.objects.all()
	todo_form = TodoForm()
	
	return render_to_response('overview.html', { 'projects': projects, 'todo_form': todo_form })


def addproject(request):
	projects = Project.objects.all()
	
	if request.POST:
		project = ProjectForm(request.POST)
		if project.is_valid():
			project.save()
	else:
		project = ProjectForm()
	
	return render_to_response('addproject.html', { 'form': project, 'projects': projects })


def addcategory(request):
	categories = Category.objects.all()
	
	if request.POST:
		category = CategoryForm(request.POST)
		if category.is_valid():
			category.save()
	else:
		category = CategoryForm()
		
	return render_to_response('addcategory.html', { 'form': category, 'categories': categories })

	
def addtodo(request):
	if request.POST:
		f = TodoForm(request.POST)
		if f.is_valid():
			todo = f.save()
			return HttpResponse(simplejson.dumps({ 'id': todo.id, 'created': todo.created }))
		
	raise Http404(repr(f.errors) if f else None)


def completetodo(request, id, complete):
	todo = get_object_or_404(Todo, pk=id)
	todo.complete = int(complete)
	todo.save()
	return HttpResponse()


def prioritize(request, id):
	if request.POST:
		category = get_object_or_404(Category, pk=id)
		for i, todo_id in enumerate(request.POST['order'].split(',')):
			todo = get_object_or_404(Todo, pk=todo_id)
			if(todo.category.id == category.id):
				todo.priority = i
				todo.save()
	return HttpResponse()