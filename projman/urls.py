from django.conf.urls.defaults import *
from models import *
from projman import views
from django.views.generic.create_update import delete_object

urlpatterns = patterns('',
	url(r'^overview/$', views.overview, name='pm_overview'),
	url(r'^addproject/$', views.addproject, name='pm_addproject'),
	url(r'^delproject/(?P<object_id>\d+)/$', delete_object, 
		{ 'model': Project, 'post_delete_redirect': '/', 'template_name': 'project_confirm_delete.html' }, name='pm_delproject'),
	url(r'^addcategory/$', views.addcategory, name='pm_addcategory'),
	url(r'^delcategory/(?P<object_id>\d+)/$', delete_object,
		{ 'model': Category, 'post_delete_redirect': '/', 'template_name': 'category_confirm_delete.html' }, name='pm_delcategory'),
	url(r'^addtodo/$', views.addtodo, name='pm_addtodo'),
	url(r'^deltodo/(?P<object_id>\d+)/$', delete_object,
		{ 'model': Todo, 'post_delete_redirect': '/', 'template_name': 'todo_confirm_delete.html' }, name='pm_deltodo'),
	url(r'^completetodo/(?P<id>\d+)/(?P<complete>[01]+)/$', views.completetodo, name='pm_completetodo'),
	url(r'^prioritize/(?P<id>\d+)/$', views.prioritize, name='pm_prioritize'),
)