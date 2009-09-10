from django.conf.urls.defaults import *
from models import *
import views

urlpatterns = patterns('',
	url(r'^home/$', views.home, name='pm_home'),
	url(r'^create/$', views.create, name='pm_create'),
	
	url(r'^addproject/$', views.addproject, name='pm_addproject'),
	url(r'^updateproject/(?P<project_id>\d+)/$', views.updateproject, name='pm_updateproject'),
	url(r'^delproject/(?P<object_id>\d+)/$', views.delete_object_referer, 
		{ 'model': Project, 'template_name': 'project_confirm_delete.html' }, name='pm_delproject'),
	
	url(r'^category/view/(?P<category_id>\d+)/$', views.view, name='pm_view'),
	url(r'^category/tasks/(?P<category_id>\d+)/$', views.tasks, name='pm_tasks'),
	url(r'^category/thread/(?P<content_id>\d+)/$', views.thread_view, { 'content_object': Category }, name='pm_thread'),

	url(r'^addcategory/$', views.addcategory, name='pm_addcategory'),
	url(r'^updatecategory/(?P<category_id>\d+)/$', views.updatecategory, name='pm_updatecategory'),
	url(r'^delcategory/(?P<object_id>\d+)/$', views.delete_object_referer,
		{ 'model': Category, 'template_name': 'category_confirm_delete.html' }, name='pm_delcategory'),
	
	url(r'^addtodo/$', views.addtodo, name='pm_addtodo'),
	url(r'^deletetodo/(?P<todo_id>\d+)/$', views.deletetodo, name='pm_deletetodo'),
	url(r'^completetodo/(?P<todo_id>\d+)/(?P<complete>[01]+)/$', views.completetodo, name='pm_completetodo'),
	url(r'^updatetodo/(?P<todo_id>\d+)/$', views.updatetodo, name='pm_updatetodo'),
	
	url(r'^addmilestone/$', views.addmilestone, name='pm_addtodo'),
	
	url(r'^load/$', views.load, name='pm_load'),
	
	url(r'^prioritize/(?P<obj_type>\w+)/(?P<id>\d+)/$', views.prioritize, name='pm_prioritize'),

	url(r'^thread/post/$', views.thread_post, name='thread_post'),
)
