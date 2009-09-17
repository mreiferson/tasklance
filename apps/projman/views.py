from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from forms import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm;
from django.utils.dateformat import *
from xml.etree import ElementTree as etree
from django.core.urlresolvers import reverse
from django.views.generic.create_update import delete_object
from decorators import useracct_required
from django.contrib.contenttypes.models import ContentType


@useracct_required
def home(request):
	category_form = CategoryForm()
	load_form = LoadForm()
	
	return render_to_response('home.html', { 'category_form': category_form, 'load_form': load_form },
		context_instance=RequestContext(request))


@useracct_required
def tasks(request, category_id):
	category = get_object_or_404(Category, pk=category_id)
	if category.account == request.account:
		todo_form = TodoForm()
		project_form = ProjectForm()
		
		return render_to_response('tasks.html', { 'category': category, 'todo_form': todo_form,
			'project_form': project_form }, context_instance=RequestContext(request))
		
	else:
		return HttpResponseRedirect(reverse('login'))
		
@useracct_required
def overview(request, category_id):
	category = get_object_or_404(Category, pk=category_id)
	if category.account == request.account:
		todos = Todo.objects.filter(project__category__exact=category)
		messages = category.get_thread().message_set.all()
		milestones = category.milestone_set.all()
		
		items = []
		for todo in todos:
			if todo.complete:
				ts = todo.completed
			else:
				ts = todo.created
			
			items.append((ts, 'todo', todo))
				
		for message in messages:
			ts = message.created
			
			items.append((ts, 'message', message))
			
		for milestone in milestones:
			ts = milestone.created
			
			items.append((ts, 'milestone', milestone))
		
		d = {}
		dateLongStrings = {}
		for l in items:
			df = DateFormat(l[0])
			dateString = df.format('Y-m-d')
			timeString = df.format('g:ia')
			item = (df.format('Gis'), timeString, l[1], l[2])
			
			if dateString in d:
				d[dateString].append(item)
			else:
				dateLongStrings[dateString] = df.format('l, F jS')
				d[dateString] = [item]
		
		items = []
		keys = d.keys()
		keys.sort(reverse=True)
		for key in keys:
			d[key].sort(reverse=True, key=lambda x: x[0])
			items.append((dateLongStrings[key], d[key]))
		
		return render_to_response('overview.html', { 'category': category, 'items': items }, 
			context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('login'))
		
@useracct_required
def thread_view(request, content_object, content_id):
	obj = get_object_or_404(content_object, pk=content_id)
	try:
		ctype = ContentType.objects.get_for_model(obj)
		thread = Thread.objects.get(content_type__pk=ctype.id, object_id=obj.id)
	except:
		thread = Thread(content_object=obj, creator=request.user)
		thread.save()
		
	msg_form = MessageForm()
	
	return render_to_response('thread_view.html', { content_object.__name__.lower(): obj, 
		'thread': thread, 'msg_form': msg_form }, context_instance=RequestContext(request))
		

def milestones(request, category_id):
	category = get_object_or_404(Category, pk=category_id)
	milestone_form = MilestoneForm()
	
	return render_to_response('milestones.html', { 'category': category, 
		'milestone_form': milestone_form }, context_instance=RequestContext(request))


def delete_object_referer(request, object_id, **kwargs):
	backup = reverse('pm_home')
	
	if request.method == 'POST':
		post_delete_redirect = request.POST.get('post_delete_redirect', backup)
	else:
		post_delete_redirect = request.META.get('HTTP_REFERER', backup)
		
	return delete_object(request, object_id=object_id, 
		post_delete_redirect=post_delete_redirect, 
		extra_context={ 'post_delete_redirect': post_delete_redirect }, 
		**kwargs)


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
			
			return HttpResponseRedirect(reverse('login'))
	
	return render_to_response('create.html', { 'usercreation_form': usercreation_form,
		'account_form': account_form }, context_instance=RequestContext(request))


def addcategory(request):
	if request.method == 'POST':
		f = CategoryForm(request.POST)
		if f.is_valid():
			category = f.save()
			return HttpResponse(simplejson.dumps({ 'id': category.id, 
				'name': category.name, 'description': category.description }))
		
	raise Http404(repr(f.errors) if f else None)
	
	
def addmilestone(request):
	if request.method == 'POST':
		f = MilestoneForm(request.POST)
		if f.is_valid():
			milestone = f.save()
			df = DateFormat(milestone.deadline)
			return HttpResponse(simplejson.dumps({ 'id': milestone.id,
				'name': milestone.name, 'description': milestone.description,
				'deadline': df.format('Y-m-d') }))
					
	raise Http404(repr(f.errors) if f else None)
	
	
def milestoneaddproject(request):
	if request.method == 'POST':
		milestone = get_object_or_404(Milestone, pk=request.POST['milestone_id'])
		project = get_object_or_404(Project, pk=request.POST['project_id'])
		
		project.milestone = milestone
		project.save()
		
		return HttpResponse(simplejson.dumps({ 'project_id': project.id, 'milestone_id': milestone.id, 'name': project.name }))
		
	raise Http404(None)


def addproject(request):
	if request.method == 'POST':
		f = ProjectForm(request.POST)
		if f.is_valid():
			project = f.save()
			return HttpResponse(simplejson.dumps({ 'id': project.id, 
				'name': project.name, 'description': project.description }))
		
	raise Http404(repr(f.errors) if f else None)


def addtodo(request):
	if request.method == 'POST':
		f = TodoForm(request.POST)
		if f.is_valid():
			todo = f.save()
			df = DateFormat(todo.created)
			return HttpResponse(simplejson.dumps({ 'id': todo.id, 
				'created': df.format('Y-m-d g:ia'), 'item': todo.item }))
		
	raise Http404(repr(f.errors) if f else None)


def updatecategory(request, category_id):
	if request.method == 'POST':
		category = get_object_or_404(Category, pk=category_id)
		
		if 'description' in request.POST:
			category.description = request.POST['description']
		
		if 'name' in request.POST:
			category.name = request.POST['name']
		
		category.save()
		
		return HttpResponse(simplejson.dumps({ 'id': category.id, 'name': category.name, 
			'description': category.description }))
			
	raise Http404(None)


def updateproject(request, project_id):
	if request.method == 'POST':
		project = get_object_or_404(Project, pk=project_id)
		
		if 'description' in request.POST:
			project.description = request.POST['description']
		
		if 'name' in request.POST:
			project.name = request.POST['name']
			
		project.save()
		
		return HttpResponse(simplejson.dumps({ 'id': project.id, 'name': project.name, 
			'description': project.description }))
	
	raise Http404(None)
	

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
		
		df = DateFormat(todo.completed if todo.completed else todo.created)
		
		return HttpResponse(simplejson.dumps({ 'id': todo.id, 
			'complete': todo.complete, 
			'date': df.format('Y-m-d g:ia'), 
			'age': todo.age().days }))
	
	raise Http404(None)
	

def updatetodo(request, todo_id):
	if request.method == 'POST':
		todo = get_object_or_404(Todo, pk=todo_id)
		project = get_object_or_404(Project, pk=request.POST['project_id'])
		todo.category = category
		todo.save()
		
		return HttpResponse(simplejson.dumps({ 'id': todo.id, 'project': todo.project.id }))
	
	raise Http404(None)
	

def prioritize(request, obj_type, id):
	if request.method == 'POST':
		parent_mapping = { 'category': Account, 'milestone': Category, 'project': Category, 'todo': Project }
		mapping = { 'category': Category, 'milestone': Milestone, 'project': Project, 'todo': Todo }
		
		obj_type = obj_type.lower()
		parent = get_object_or_404(parent_mapping[obj_type], pk=id)
		order = request.POST['order'].split(',')
		for i, obj_id in enumerate(order):
			obj = get_object_or_404(mapping[obj_type], pk=obj_id)
			if getattr(obj, parent.__class__.__name__.lower()).id == parent.id:
				obj.priority = i
				obj.save()

	return HttpResponse(simplejson.dumps({ 'id': parent.id, 'order': order }))


def thread_post(request):
	if request.method == 'POST':
		f = MessageForm(request.POST)
		if f.is_valid():
			t = f.save(commit=False)
			t.creator = request.user
			t.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def load(request):
	if request.method == 'POST':
		f = LoadForm(request.POST, request.FILES)
		if f.is_valid():
			account = Account.objects.filter(useraccount__user__exact=request.user)[0]
			
			doc = etree.fromstring(request.FILES['file'].read())
			projects = doc.findall('projects/project')
			for project in projects:
				name = project.findtext('name')
				
				p = Project(account=account, name=name, description='')
				p.save()
				
				todolists = project.findall('todo-lists/todo-list')
				for todolist in todolists:
					name = todolist.findtext('name')
					description = todolist.findtext('description')
					
					c = Category(project=p, name=name, description=description)
					c.save()
					
					todoitems = todolist.findall('todo-items/todo-item')
					for todoitem in todoitems:
						item = todoitem.findtext('content')[:255]
						created = datetime.strptime(todoitem.findtext('created-on'), 
								'%Y-%m-%dT%H:%M:%SZ')
						complete = (todoitem.findtext('completed') == 'true')
						completed = datetime.strptime(todoitem.findtext('completed-on'), 
								'%Y-%m-%dT%H:%M:%SZ') if complete else None
						priority = todoitem.findtext('position')
						
						t = Todo(category=c, item=item, created=created, complete=complete, 
							completed=completed, priority=priority)
						t.save()
		
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('pm_home')))
	
	return render_to_response('load.html')
