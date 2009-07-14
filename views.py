from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm;
from django.contrib.auth.models import User;
from django.contrib import auth
from django.template import RequestContext


def index(request):
	register_form = UserCreationForm()
	login_form = AuthenticationForm()
	
	return render_to_response('index.html', { 'register_form': register_form, 
		'login_form': login_form }, context_instance=RequestContext(request))


def register(request):
	f = UserCreationForm()
	
	if request.POST:
		f = UserCreationForm(request.POST)
		if f.is_valid():
			user = f.save()
			return HttpResponseRedirect('/login')
	
	return render_to_response('register.html', { 'register_form': f },
		context_instance=RequestContext(request))


def login(request):
	f = AuthenticationForm()
	
	if request.POST:
		f = AuthenticationForm(data=request.POST)
		if f.is_valid():
			user = f.get_user()
			auth.login(request, user)
			return HttpResponseRedirect('/pm/overview')
				
	return render_to_response('login.html', { 'login_form': f },
		context_instance=RequestContext(request))
		
def logout(request):
	auth.logout(request)
	
	return HttpResponseRedirect('/')