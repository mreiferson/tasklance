from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from forms import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm;
from django.utils.dateformat import *


@login_required
def overview(request):
	accounts = Account.objects.filter(useraccount__user__exact=request.user)
	
	return render_to_response('overview.html', { 'accounts': accounts },
		context_instance=RequestContext(request))


@login_required
def view(request, account_id):
	account = get_object_or_404(Account, pk=account_id)
	if account.useraccount_set.filter(user__exact=request.user) != []:
		projects = account.project_set.all()
		todo_form = TodoForm()
		project_form = ProjectForm()
		category_form = CategoryForm()
		
		return render_to_response('view.html', { 'account': account, 'projects': projects, 
			'todo_form': todo_form, 'project_form': project_form, 
			'category_form': category_form }, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login')


def create(request):
	usercreation_form = UserCreationForm(prefix='user')
	account_form = AccountForm(prefix='acct')
	
	if request.method == 'POST':
		usercreation_form = UserCreationForm(request.POST, prefix='user')
		account_form = AccountForm(request.POST, prefix='acct')
		if usercreation_form.is_valid() and account_form.is_valid():
			user = usercreation_form.save()
			account = account_form.save()
			useraccount = UserAccount()
			useraccount.user = user
			useraccount.account = account
			useraccount.save()
			
			return HttpResponseRedirect('/login')
	
	return render_to_response('create.html', { 'usercreation_form': usercreation_form,
		'account_form': account_form }, context_instance=RequestContext(request))


def addproject(request):
	if request.method == 'POST':
		f = ProjectForm(request.POST)
		if f.is_valid():
			project = f.save()
			return HttpResponse(simplejson.dumps({ 'id': project.id, 
				'name': project.name, 'description': project.description }))
		
	raise Http404(repr(f.errors) if f else None)


def updateproject(request, project_id):
	if request.method == 'POST':
		project = get_object_or_404(Project, pk=project_id)
		project.description = request.POST['description']
		project.save()
		
		return HttpResponse(simplejson.dumps({ 'id': project.id, 'description': project.description }))
	
	raise Http404(None)


def addcategory(request):
	if request.method == 'POST':
		f = CategoryForm(request.POST)
		if f.is_valid():
			category = f.save()
			return HttpResponse(simplejson.dumps({ 'id': category.id, 
				'project_id': category.project.id, 'name': category.name, 'description': category.description }))
		
	raise Http404(repr(f.errors) if f else None)
	

def updatecategory(request, category_id):
	if request.method == 'POST':
		category = get_object_or_404(Category, pk=category_id)
		category.description = request.POST['description']
		category.save()
		
		return HttpResponse(simplejson.dumps({ 'id': category.id, 'description': category.description }))
			
	raise Http404(None)

	
def addtodo(request):
	if request.method == 'POST':
		f = TodoForm(request.POST)
		if f.is_valid():
			todo = f.save()
			df = DateFormat(todo.created)
			return HttpResponse(simplejson.dumps({ 'id': todo.id, 
				'created': df.format('Y-m-d g:ia'), 'item': todo.item }))
		
	raise Http404(repr(f.errors) if f else None)
	

def deletetodo(request, todo_id):
	if request.method == 'POST':
		todo = get_object_or_404(Todo, pk=todo_id)
		todo.delete()
		
		return HttpResponse(simplejson.dumps({ 'return': True }))
			
	raise Http404(None)


def completetodo(request, todo_id, complete):
	if request.method == 'POST':
		todo = get_object_or_404(Todo, pk=todo_id)
		todo.complete = int(complete)
		todo.save()
		
		return HttpResponse(simplejson.dumps({ 'id': todo.id, 'complete': todo.complete, 'date': (todo.complete and todo.completed or todo.created).strftime('%Y-%m-%d %H:%M:%S') }))
	
	raise Http404(None)
	

def updatetodo(request, todo_id):
	if request.method == 'POST':
		todo = get_object_or_404(Todo, pk=todo_id)
		category = get_object_or_404(Category, pk=request.POST['category_id'])
		todo.category = category
		todo.save()
		
		return HttpResponse(simplejson.dumps({ 'id': todo.id, 'category': todo.category.id }))
	
	raise Http404(None)


def prioritize(request, id):
	if request.method == 'POST':
		category = get_object_or_404(Category, pk=id)
		for i, todo_id in enumerate(request.POST['order'].split(',')):
			todo = get_object_or_404(Todo, pk=todo_id)
			if(todo.category.id == category.id):
				todo.priority = i
				todo.save()
	
	return HttpResponse(simplejson.dumps({ 'id': category.id, 'order': request.POST['order'].split(',') }))