from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from forms import *
from django.db import connection

def overview(request):
	projects = Project.objects.all()
	
	return render_to_response('overview.html', { 'projects': projects })

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
	todos = Todo.objects.all()

	if request.POST:
		todo = TodoForm(request.POST)
		if todo.is_valid():
			todo.save()
	else:
		todo = TodoForm()

	return render_to_response('addtodo.html', { 'form': todo, 'projects': todos })
	
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