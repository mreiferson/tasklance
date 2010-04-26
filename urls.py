from django.contrib import admin
from django.conf.urls.defaults import *
from django.conf import settings
import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    url(r'^pm/', include('projman.urls')),
    url(r'^admin/(.*)', admin.site.root)
)
