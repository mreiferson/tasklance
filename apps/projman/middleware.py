import re
from models import Account

class SubdomainMiddleware(object):
	def process_request(self, request):
		m = re.match('(?P<subdomain>\w+)\..*', request.META['SERVER_NAME'])
		subdomain = m.group('subdomain')
		try:
			account = Account.objects.get(subdomain__exact=subdomain)
			request.account = account
		except:
			request.account = None

		return None
		
	#def process_view(self, request, view_func, view_args, view_kwargs):
		
	#def process_response(self, request, response):
		
	#def process_exception(self, request, exception):