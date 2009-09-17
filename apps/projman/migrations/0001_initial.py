
from south.db import db
from django.db import models
from projman.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserAccount'
        db.create_table('projman_useraccount', (
            ('id', orm['projman.UserAccount:id']),
            ('user', orm['projman.UserAccount:user']),
            ('account', orm['projman.UserAccount:account']),
        ))
        db.send_create_signal('projman', ['UserAccount'])
        
        # Adding model 'Task'
        db.create_table('projman_task', (
            ('id', orm['projman.Task:id']),
            ('project', orm['projman.Task:project']),
            ('item', orm['projman.Task:item']),
            ('complete', orm['projman.Task:complete']),
            ('priority', orm['projman.Task:priority']),
            ('created', orm['projman.Task:created']),
            ('completed', orm['projman.Task:completed']),
        ))
        db.send_create_signal('projman', ['Task'])
        
        # Adding model 'Milestone'
        db.create_table('projman_milestone', (
            ('id', orm['projman.Milestone:id']),
            ('category', orm['projman.Milestone:category']),
            ('name', orm['projman.Milestone:name']),
            ('description', orm['projman.Milestone:description']),
            ('deadline', orm['projman.Milestone:deadline']),
            ('created', orm['projman.Milestone:created']),
            ('priority', orm['projman.Milestone:priority']),
        ))
        db.send_create_signal('projman', ['Milestone'])
        
        # Adding model 'Account'
        db.create_table('projman_account', (
            ('id', orm['projman.Account:id']),
            ('name', orm['projman.Account:name']),
            ('description', orm['projman.Account:description']),
            ('subdomain', orm['projman.Account:subdomain']),
            ('created', orm['projman.Account:created']),
        ))
        db.send_create_signal('projman', ['Account'])
        
        # Adding model 'Message'
        db.create_table('projman_message', (
            ('id', orm['projman.Message:id']),
            ('thread', orm['projman.Message:thread']),
            ('text', orm['projman.Message:text']),
            ('creator', orm['projman.Message:creator']),
            ('created', orm['projman.Message:created']),
        ))
        db.send_create_signal('projman', ['Message'])
        
        # Adding model 'Thread'
        db.create_table('projman_thread', (
            ('id', orm['projman.Thread:id']),
            ('content_type', orm['projman.Thread:content_type']),
            ('object_id', orm['projman.Thread:object_id']),
            ('creator', orm['projman.Thread:creator']),
            ('created', orm['projman.Thread:created']),
        ))
        db.send_create_signal('projman', ['Thread'])
        
        # Adding model 'Dependency'
        db.create_table('projman_dependency', (
            ('id', orm['projman.Dependency:id']),
            ('task_a', orm['projman.Dependency:task_a']),
            ('task_b', orm['projman.Dependency:task_b']),
        ))
        db.send_create_signal('projman', ['Dependency'])
        
        # Adding model 'Category'
        db.create_table('projman_category', (
            ('id', orm['projman.Category:id']),
            ('account', orm['projman.Category:account']),
            ('name', orm['projman.Category:name']),
            ('description', orm['projman.Category:description']),
            ('created', orm['projman.Category:created']),
            ('priority', orm['projman.Category:priority']),
        ))
        db.send_create_signal('projman', ['Category'])
        
        # Adding model 'Project'
        db.create_table('projman_project', (
            ('id', orm['projman.Project:id']),
            ('category', orm['projman.Project:category']),
            ('milestone', orm['projman.Project:milestone']),
            ('name', orm['projman.Project:name']),
            ('description', orm['projman.Project:description']),
            ('created', orm['projman.Project:created']),
            ('priority', orm['projman.Project:priority']),
        ))
        db.send_create_signal('projman', ['Project'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserAccount'
        db.delete_table('projman_useraccount')
        
        # Deleting model 'Task'
        db.delete_table('projman_task')
        
        # Deleting model 'Milestone'
        db.delete_table('projman_milestone')
        
        # Deleting model 'Account'
        db.delete_table('projman_account')
        
        # Deleting model 'Message'
        db.delete_table('projman_message')
        
        # Deleting model 'Thread'
        db.delete_table('projman_thread')
        
        # Deleting model 'Dependency'
        db.delete_table('projman_dependency')
        
        # Deleting model 'Category'
        db.delete_table('projman_category')
        
        # Deleting model 'Project'
        db.delete_table('projman_project')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'projman.account': {
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'projman.category': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projman.Account']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'projman.dependency': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task_a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'depends_on'", 'to': "orm['projman.Task']"}),
            'task_b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dependency_of'", 'to': "orm['projman.Task']"})
        },
        'projman.message': {
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'msg'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projman.Thread']"})
        },
        'projman.milestone': {
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projman.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'projman.project': {
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projman.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projman.Milestone']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'projman.task': {
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projman.Project']"})
        },
        'projman.thread': {
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'projman.useraccount': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projman.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }
    
    complete_apps = ['projman']
