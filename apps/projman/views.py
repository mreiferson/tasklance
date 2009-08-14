from django.http import	HttpResponse, HttpResponseRedirect,	Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from forms import *
from django.contrib.auth.decorators	import login_required
from django.template import	RequestContext
from django.contrib.auth.forms import UserCreationForm,	AuthenticationForm;
from django.utils.dateformat import	*
from xml.etree import ElementTree as etree
from django.core.urlresolvers import reverse
from django.views.generic.create_update import delete_object


@login_required
def	overview(request):
	accounts = Account.objects.filter(useraccount__user__exact=request.user)
	
	return render_to_response('overview.html', { 'accounts': accounts },
		context_instance=RequestContext(request))


@login_required
def	view(request, account_id):
	account	= get_object_or_404(Account, pk=account_id)
	if account.useraccount_set.filter(user__exact=request.user).count():
		projects = account.project_set.all()
		todo_form =	TodoForm()
		project_form = ProjectForm()
		category_form =	CategoryForm()
		load_form = LoadForm()
		
		return render_to_response('view.html', { 'account':	account, 'projects': projects, 
			'todo_form': todo_form,	'project_form':	project_form, 
			'category_form': category_form, 'load_form': load_form }, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login')


def delete_object_referer(request, object_id, **kwargs):
	backup = reverse('pm_overview')
	
	if request.method == 'POST':
		post_delete_redirect = request.POST.get('post_delete_redirect', backup)
	else:
		post_delete_redirect = request.META.get('HTTP_REFERER', backup)
		
	return delete_object(request, object_id=object_id, 
		post_delete_redirect=post_delete_redirect, 
		extra_context={ 'post_delete_redirect': post_delete_redirect }, 
		**kwargs)


def	create(request):
	usercreation_form =	UserCreationForm(prefix='user')
	account_form = AccountForm(prefix='acct')
	
	if request.method == 'POST':
		usercreation_form =	UserCreationForm(request.POST, prefix='user')
		account_form = AccountForm(request.POST, prefix='acct')
		if usercreation_form.is_valid()	and	account_form.is_valid():
			user = usercreation_form.save()
			account	= account_form.save()
			useraccount	= UserAccount()
			useraccount.user = user
			useraccount.account	= account
			useraccount.save()
			
			return HttpResponseRedirect('/login')
	
	return render_to_response('create.html', { 'usercreation_form':	usercreation_form,
		'account_form':	account_form },	context_instance=RequestContext(request))


def	addproject(request):
	if request.method == 'POST':
		f =	ProjectForm(request.POST)
		if f.is_valid():
			project	= f.save()
			return HttpResponse(simplejson.dumps({ 'id': project.id, 
				'name':	project.name, 'description': project.description }))
		
	raise Http404(repr(f.errors) if	f else None)


def	updateproject(request, project_id):
	if request.method == 'POST':
		project	= get_object_or_404(Project, pk=project_id)
		
		if 'description' in request.POST:
			project.description = request.POST['description']
		
		if 'name' in request.POST:
			project.name = request.POST['name']
			
		project.save()
		
		return HttpResponse(simplejson.dumps({ 'id': project.id, 'name': project.name, 'description': project.description }))
	
	raise Http404(None)


def	addcategory(request):
	if request.method == 'POST':
		f =	CategoryForm(request.POST)
		if f.is_valid():
			category = f.save()
			return HttpResponse(simplejson.dumps({ 'id': category.id, 
				'project_id': category.project.id, 'name': category.name, 'description': category.description }))
		
	raise Http404(repr(f.errors) if	f else None)
	

def	updatecategory(request,	category_id):
	if request.method == 'POST':
		category = get_object_or_404(Category, pk=category_id)
		
		if 'description' in request.POST:
			category.description = request.POST['description']
		
		if 'name' in request.POST:
			category.name = request.POST['name']
		
		category.save()
		
		return HttpResponse(simplejson.dumps({ 'id': category.id, 'name': category.name, 'description': category.description }))
			
	raise Http404(None)

	
def	addtodo(request):
	if request.method == 'POST':
		f =	TodoForm(request.POST)
		if f.is_valid():
			todo = f.save()
			df = DateFormat(todo.created)
			return HttpResponse(simplejson.dumps({ 'id': todo.id, 
				'created': df.format('Y-m-d	g:ia'),	'item':	todo.item }))
		
	raise Http404(repr(f.errors) if	f else None)
	

def	deletetodo(request,	todo_id):
	if request.method == 'POST':
		todo = get_object_or_404(Todo, pk=todo_id)
		todo.delete()
		
		return HttpResponse(simplejson.dumps({ 'return': True }))
			
	raise Http404(None)


def	completetodo(request, todo_id, complete):
	if request.method == 'POST':
		todo = get_object_or_404(Todo, pk=todo_id)
		todo.complete =	int(complete)
		todo.save()
		
		df = DateFormat(todo.completed if todo.completed else todo.created)
		
		return HttpResponse(simplejson.dumps({ 'id': todo.id, 
			'complete': todo.complete, 
			'date': df.format('Y-m-d g:ia'), 
			'age': todo.age().days }))
	
	raise Http404(None)
	

def	updatetodo(request,	todo_id):
	if request.method == 'POST':
		todo = get_object_or_404(Todo, pk=todo_id)
		category = get_object_or_404(Category, pk=request.POST['category_id'])
		todo.category =	category
		todo.save()
		
		return HttpResponse(simplejson.dumps({ 'id': todo.id, 'category': todo.category.id }))
	
	raise Http404(None)


def	load(request):
	if request.method == 'POST':
		f = LoadForm(request.POST, request.FILES)
		if f.is_valid():
			account = Account.objects.filter(useraccount__user__exact=request.user)[0]
			
			doc	= etree.fromstring(request.FILES['file'].read())
			projects = doc.findall('projects/project')
			for	project	in projects:
				name = project.findtext('name')
				
				p = Project(account=account, name=name, description='')
				p.save()
				
				todolists =	project.findall('todo-lists/todo-list')
				for	todolist in	todolists:
					name = todolist.findtext('name')
					description = todolist.findtext('description')
					
					c = Category(project=p, name=name, description=description)
					c.save()
					
					todoitems =	todolist.findall('todo-items/todo-item')
					for	todoitem in	todoitems:
						item = todoitem.findtext('content')[:255]
						created = datetime.strptime(todoitem.findtext('created-on'), '%Y-%m-%dT%H:%M:%SZ')
						complete = (todoitem.findtext('completed') == 'true')
						completed = datetime.strptime(todoitem.findtext('completed-on'), '%Y-%m-%dT%H:%M:%SZ') if complete else None
						priority = todoitem.findtext('position')
						
						t = Todo(category=c, item=item, created=created, complete=complete, completed=completed, priority=priority)
						t.save()
								
		
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('pm_overview')))
	
	return render_to_response('load.html')


def	prioritize(request,	id):
	if request.method == 'POST':
		category = get_object_or_404(Category, pk=id)
		order = request.POST['order'].split(',')
		for	i, todo_id in enumerate(order):
			todo = get_object_or_404(Todo, pk=todo_id)
			if todo.category.id	== category.id:
				todo.priority =	i
				todo.save()
	
	return HttpResponse(simplejson.dumps({ 'id': category.id, 'order': order }))
	

def prioritize_project(request, id):
	if request.method == 'POST':
		project = get_object_or_404(Project, pk=id)
		order = request.POST['order'].split(',')
		for i, category_id in enumerate(order):
			category = get_object_or_404(Category, pk=category_id)
			if category.project.id == project.id:
				category.priority = i
				category.save()
				
	return HttpResponse(simplejson.dumps({ 'id': project.id, 'order': order	}))
	

def prioritize_account(request, id):
	if request.method == 'POST':
		account = get_object_or_404(Account, pk=id)
		order = request.POST['order'].split(',')
		for i, project_id in enumerate(order):
			project = get_object_or_404(Project, pk=project_id)
			if project.account.id == account.id:
				project.priority = i
				project.save()
	
	return HttpResponse(simplejson.dumps({ 'id': account.id, 'order': order	}))