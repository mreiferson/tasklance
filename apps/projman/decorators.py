from django.http import    HttpResponse, HttpResponseRedirect,    Http404
from django.core.urlresolvers import reverse
from models import Account

def useracct_required(f):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated() and request.account.useraccount_set.filter(user__exact=request.user).count():
            return f(request, *args, **kwargs)
        
        return HttpResponseRedirect(reverse('login'))
    
    return wrap
