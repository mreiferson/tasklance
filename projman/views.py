from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from forms import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm;


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
	
	if request.POST:
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
	if request.POST:
		f = ProjectForm(request.POST)
		if f.is_valid():
			project = f.save()
			return HttpResponse(simplejson.dumps({ 'id': project.id, 
				'name': project.name }))
		
	raise Http404(repr(f.errors) if f else None)


def addcategory(request):
	if request.POST:
		f = CategoryForm(request.POST)
		if f.is_valid():
			category = f.save()
			return HttpResponse(simplejson.dumps({ 'id': category.id, 
				'project_id': category.project.id, 'name': category.name }))
		
	raise Http404(repr(f.errors) if f else None)

	
def addtodo(request):
	if request.POST:
		f = TodoForm(request.POST)
		if f.is_valid():
			todo = f.save()
			return HttpResponse(simplejson.dumps({ 'id': todo.id, 
				'created': todo.created.strftime('%Y-%m-%d %H:%M:%S'), 'item': todo.item }))
		
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