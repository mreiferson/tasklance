from django.http import    HttpResponse, HttpResponseRedirect,    Http404
import re
from models import Account

class SubdomainMiddleware(object):
    def process_request(self, request):
        account = Account()
        
        subdomain = request.GET.get('_subdomain')
        if subdomain is None:
            m = re.match('(?P<subdomain>\w+)\.(?P<domain>.*\..*)', request.META['SERVER_NAME'])
            if m is not None:
                subdomain = m.group('subdomain')
        
        url = request.META['SERVER_NAME']+(':'+request.META['SERVER_PORT'] if (request.META['SERVER_PORT'] != '80') else '')
        if subdomain is None:
            return HttpResponseRedirect('http://www.'+url);
        
        if subdomain != 'www':
            try:
                account = Account.objects.get(subdomain__exact=subdomain)
            except:
                return HttpResponseRedirect('http://'+url)
        
        request.subdomain = subdomain
        request.account = account
        
        return None
        
    #def process_view(self, request, view_func, view_args, view_kwargs):
        
    #def process_response(self, request, response):
        
    #def process_exception(self, request, exception):
