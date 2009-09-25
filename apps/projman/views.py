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
from django.template.loader import get_template


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
		task_form = TaskForm()
		project_form = ProjectForm()
		
		return render_to_response('tasks.html', { 'category': category, 'task_form': task_form,
			'project_form': project_form }, context_instance=RequestContext(request))
		
	else:
		return HttpResponseRedirect(reverse('login'))


@useracct_required
def overview(request, category_id):
	category = get_object_or_404(Category, pk=category_id)
	if category.account == request.account:
		tasks = Task.objects.filter(project__category__exact=category)
		
		try: 
			messages = category.get_thread().message_set.all()
		except Thread.DoesNotExist:
			messages = []
			
		milestones = category.milestone_set.all()
		
		items = []
		[items.append((t.completed if t.complete else t.created, 'task', t)) for t in tasks]
		[items.append((m.created, 'message', m)) for m in messages]
		[items.append((m.created, 'milestone', m)) for m in milestones]
		
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
		'milestone_status': (('onhold', 'On Hold'), ('active', 'Active'), ('complete', 'Complete')),
		'milestone_form': milestone_form }, context_instance=RequestContext(request))


def milestonestatus(request):
	if request.method == 'POST':
		milestone = get_object_or_404(Milestone, pk=request.POST['milestone_id'])
		milestone.status = request.POST['status']
		milestone.save()
		
		return HttpResponse(simplejson.dumps({ 'milestone_id': milestone.id, 'status': milestone.status}))
	
	raise Http404(None)


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
	
	
def delmilestone(request, milestone_id):
	if request.method == 'POST':
		milestone = get_object_or_404(Milestone, pk=milestone_id)
		milestone.delete()
		
		return HttpResponse(simplejson.dumps({ 'return': True }))
		
	raise Http404(None)
	
	
def addprojecttomilestone(request):
	if request.method == 'POST':
		milestone = get_object_or_404(Milestone, pk=request.POST['milestone_id'])
		project = get_object_or_404(Project, pk=request.POST['project_id'])
		
		milestone.projects.add(project)
		
		return HttpResponse(simplejson.dumps({ 'project_id': project.id, 
			'milestone_id': milestone.id, 'name': project.name, 
			'perc_completed': "%.2f" % project.perc_completed(), 'milestone_perc_completed': "%.2f" % milestone.perc_completed() }))
		
	raise Http404(None)
	
	
def delprojectfrommilestone(request):
	if request.method == 'POST':
		project = get_object_or_404(Project, pk=request.POST['project_id'])
		milestone = get_object_or_404(Milestone, pk=request.POST['milestone_id'])
		
		milestone.projects.remove(project)
		
		return HttpResponse(simplejson.dumps({ 'milestone_perc_completed': "%.2f" % milestone.perc_completed() }))
		
	raise Http404(None)


def addproject(request):
	if request.method == 'POST':
		f = ProjectForm(request.POST)
		if f.is_valid():
			project = f.save()
			return HttpResponse(simplejson.dumps({ 'id': project.id, 
				'name': project.name, 'description': project.description }))
		
	raise Http404(repr(f.errors) if f else None)


def addtask(request):
	if request.method == 'POST':
		f = TaskForm(request.POST)
		if f.is_valid():
			task = f.save()
			df = DateFormat(task.created)
			return HttpResponse(simplejson.dumps({ 'id': task.id, 
				'created': df.format('Y-m-d g:ia'), 'item': task.item }))
		
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
	

def deletetask(request, task_id):
	if request.method == 'POST':
		task = get_object_or_404(Task, pk=task_id)
		task.delete()
		
		return HttpResponse(simplejson.dumps({ 'return': True }))
			
	raise Http404(None)


def completetask(request, task_id, complete):
	if request.method == 'POST':
		task = get_object_or_404(Task, pk=task_id)
		task.complete = int(complete)
		task.save()
		
		df = DateFormat(task.completed if task.completed else task.created)
		
		return HttpResponse(simplejson.dumps({ 'id': task.id, 
			'complete': task.complete, 
			'date': df.format('Y-m-d g:ia'), 
			'age': task.age().days }))
	
	raise Http404(None)
	

def updatetask(request, task_id):
	if request.method == 'POST':
		task = get_object_or_404(Task, pk=task_id)
		project = get_object_or_404(Project, pk=request.POST['project_id'])
		task.project = project
		task.save()
		
		return HttpResponse(simplejson.dumps({ 'id': task.id, 'project': task.project.id }))
	
	raise Http404(None)
	

def prioritize(request, obj_type, id):
	if request.method == 'POST':
		parent_mapping = { 'category': Account, 'milestone': Category, 'project': Category, 'task': Project }
		mapping = { 'category': Category, 'milestone': Milestone, 'project': Project, 'task': Task }
		
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
				
				tasklists = project.findall('task-lists/task-list')
				for tasklist in tasklists:
					name = tasklist.findtext('name')
					description = tasklist.findtext('description')
					
					c = Category(project=p, name=name, description=description)
					c.save()
					
					taskitems = tasklist.findall('task-items/task-item')
					for taskitem in taskitems:
						item = taskitem.findtext('content')[:255]
						created = datetime.strptime(taskitem.findtext('created-on'), 
								'%Y-%m-%dT%H:%M:%SZ')
						complete = (taskitem.findtext('completed') == 'true')
						completed = datetime.strptime(taskitem.findtext('completed-on'), 
								'%Y-%m-%dT%H:%M:%SZ') if complete else None
						priority = taskitem.findtext('position')
						
						t = Task(category=c, item=item, created=created, complete=complete, 
							completed=completed, priority=priority)
						t.save()
		
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('pm_home')))
	
	return render_to_response('load.html')
	
	
def report_weekly(request):
	t = get_template('report_weekly.html')
	html = t.render(RequestContext(request))
	
	import re
	cre = re.compile(r'(src|href)\s*=\s*"(?!http)\/([^""\'>]+)"')
	fqdn = 'http://'+request.META['SERVER_NAME']+':'+request.META['SERVER_PORT']
	html = cre.sub(r'\1="'+fqdn+r'/\2"', html)
	
	import tempfile
	s_path = tempfile.mktemp()+'.html'
	d_path = tempfile.mktemp()+'.pdf'
	
	s = open(s_path, 'w')
	s.write(html)
	s.close()
	
	import os
	cmd = '/usr/local/bin/wkhtmltopdf --print-media-type --margin-bottom 0mm --margin-top 0mm --margin-left 0mm --margin-right 0mm --page-size Letter '+s_path+' '+d_path
	p = os.system(cmd)
	
	os.unlink(s_path)
	
	o = open(d_path, 'r')
	pdf = o.read()
	o.close()
	
	os.unlink(d_path)
	
	response = HttpResponse(pdf, content_type='application/pdf')
	response['Content-disposition'] = 'attachment; filename=report.pdf'
	return response
	#return HttpResponse(html)