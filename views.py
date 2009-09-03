from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm;
from django.contrib.auth.models import User;
from django.contrib import auth
from django.template import RequestContext
from datetime import timedelta
from django.core.urlresolvers import reverse


def index(request):
	login_form = AuthenticationForm()
	
	if request.subdomain != 'www':
		template = 'login.html'	
	else:
		template = 'index.html'
		
	return render_to_response(template, { 'login_form': login_form },
		context_instance=RequestContext(request))


def login(request):
	f = AuthenticationForm()
	
	if request.POST:
		f = AuthenticationForm(data=request.POST)
		if f.is_valid():
			user = f.get_user()
			auth.login(request, user)
			request.session.set_expiry(timedelta(weeks=2) if ('remember' in request.POST) else 0)
			return HttpResponseRedirect(reverse('pm_overview'))
				
	return render_to_response('login.html', { 'login_form': f },
		context_instance=RequestContext(request))

		
def logout(request):
	auth.logout(request)
	
	return HttpResponseRedirect('/')