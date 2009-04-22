from django.contrib import admin
from django.conf.urls.defaults import *
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'django.views.generic.simple.direct_to_template', { 'template': 'index.html' }),
	url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
	url(r'^pm/', include('projman.urls')),
	url(r'^admin/(.*)', admin.site.root)
)
