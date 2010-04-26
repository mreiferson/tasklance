from django.conf.urls.defaults import *
from models import *
import views

urlpatterns = patterns('',
    url(r'^home/$', views.home, name='pm_home'),
    url(r'^create/$', views.create, name='pm_create'),
    url(r'^load/$', views.load, name='pm_load'),
    url(r'^prioritize/(?P<obj_type>\w+)/(?P<id>\d+)/$', views.prioritize, name='pm_prioritize'),
    url(r'^thread/post/$', views.thread_post, name='thread_post'),
    
    url(r'^addproject/$', views.addproject, name='pm_addproject'),
    url(r'^updateproject/(?P<project_id>\d+)/$', views.updateproject, name='pm_updateproject'),
    url(r'^delproject/(?P<object_id>\d+)/$', views.delete_object_referer, 
        { 'model': Project, 'template_name': 'project_confirm_delete.html' }, name='pm_delproject'),
    
    url(r'^addcategory/$', views.addcategory, name='pm_addcategory'),
    url(r'^updatecategory/(?P<category_id>\d+)/$', views.updatecategory, name='pm_updatecategory'),
    url(r'^delcategory/(?P<object_id>\d+)/$', views.delete_object_referer,
        { 'model': Category, 'template_name': 'category_confirm_delete.html' }, name='pm_delcategory'),
    
    url(r'^addtask/$', views.addtask, name='pm_addtask'),
    url(r'^deletetask/(?P<task_id>\d+)/$', views.deletetask, name='pm_deletetask'),
    url(r'^completetask/(?P<task_id>\d+)/(?P<complete>[01]+)/$', views.completetask, name='pm_completetask'),
    url(r'^updatetask/(?P<task_id>\d+)/$', views.updatetask, name='pm_updatetask'),
    
    url(r'^category/overview/(?P<category_id>\d+)/$', views.overview, name='pm_overview'),
    url(r'^category/tasks/(?P<category_id>\d+)/$', views.tasks, name='pm_tasks'),
    url(r'^category/thread/(?P<content_id>\d+)/$', views.thread_view, { 'content_object': Category }, name='pm_thread'),
    url(r'^category/milestones/(?P<category_id>\d+)/$', views.milestones, name='pm_milestones'),
    
    url(r'^milestone/add/$', views.addmilestone, name='pm_addmilestone'),
    url(r'^milestone/addproject/$', views.addprojecttomilestone, name='pm_addprojecttomilestone'),
    url(r'^milestone/delproject/$', views.delprojectfrommilestone, name='pm_delprojectfrommilestone'),
    url(r'^milestone/delete/(?P<object_id>\d+)/$', views.delete_object_referer, 
        { 'model': Milestone, 'template_name': 'milestone_confirm_delete.html' }, name='pm_delmilestone'),
    url(r'^milestone/status/$', views.milestonestatus, name='pm_milestonestatus'),
    url(r'^milestone/update/(?P<milestone_id>\d+)/$', views.updatemilestone, name='pm_updatemilestone'),
    
    url(r'^report/weekly/$', views.report_weekly, name='pm_report_weekly'),
)
