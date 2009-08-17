from django.http import	HttpResponse, HttpResponseRedirect,	Http404
import re
from models import Account

class SubdomainMiddleware(object):
	def process_request(self, request):
		m = re.match('(?P<subdomain>\w+)\..*', request.META['SERVER_NAME'])
		subdomain = m.group('subdomain')
		if subdomain != 'www':
			try:
				account = Account.objects.get(subdomain__exact=subdomain)
			except:
				return HttpResponseRedirect('http://www.tasklance.com'+(':'+request.META['SERVER_PORT'] if (request.META['SERVER_PORT'] != '80') else ''));
		else:
			account = Account()
		
		request.account = account
		
		return None
		
	#def process_view(self, request, view_func, view_args, view_kwargs):
		
	#def process_response(self, request, response):
		
	#def process_exception(self, request, exception):