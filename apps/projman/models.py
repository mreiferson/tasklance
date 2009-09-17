from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Account(models.Model):
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	subdomain = models.CharField(max_length=25)
	created = models.DateTimeField('Date Created', editable=False)
	
	def save(self):
		if not self.created:
			self.created = datetime.now()
		
		super(Account, self).save()
	
	def __unicode__(self):
		return self.name


class Category(models.Model):
	account = models.ForeignKey(Account)
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	created = models.DateTimeField('Date Created', editable=False)
	priority = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ('priority', 'created')
		verbose_name_plural = 'categories'
		
	def get_thread(self):
		ctype = ContentType.objects.get_for_model(self)
		return Thread.objects.get(content_type__pk=ctype.id, object_id=self.id)

	def save(self):
		if not self.created:
			self.created = datetime.now()
		
		super(Category, self).save()

	def __unicode__(self):
		return self.name+' ('+self.account.name+')'
		
		
class Milestone(models.Model):
	category = models.ForeignKey(Category)
	name = models.CharField(max_length=255)
	description = models.TextField()
	deadline = models.DateTimeField()
	created = models.DateTimeField('Date Created', editable=False)
	priority = models.PositiveIntegerField(default=0)
	
	class Meta:
		ordering = ('priority', 'created')
		
	def days_remaining(self):
		return self.deadline - datetime.now()
		
	def perc_completed(self):
		t = 0
		c = 0
		for project in self.project_set.all():
			t = t + project.perc_completed()
			c = c + 1
			
		return (float(t) / float(c)) if c else 0.0
	
	def save(self):
		if not self.created:
			self.created = datetime.now()
		
		super(Milestone, self).save()
		
	def __unicode__(self):
		return self.name+' ('+self.category.name+')'


class Project(models.Model):
	category = models.ForeignKey(Category)
	milestone = models.ForeignKey(Milestone)
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	created = models.DateTimeField('Date Created', editable=False)
	priority = models.PositiveIntegerField(default=0)
	
	class Meta:
		ordering = ('priority', 'created')
		
	def perc_completed(self):
		t = 0
		c = 0
		for task in self.task_set.all():
			if task.complete:
				c = c + 1
			t = t + 1
			
		return (float(c) / float(t) * 100.00) if t else 0.0
	
	def save(self):
		if not self.created:
			self.created = datetime.now()
		super(Project, self).save()
		
	def __unicode__(self):
		return self.name+' ('+self.category.name+')'


class Task(models.Model):
	project = models.ForeignKey(Project)
	item = models.CharField(max_length=255)
	complete = models.BooleanField(default=False)
	priority = models.PositiveIntegerField(default=0)
	created = models.DateTimeField('Creation Stamp', editable=False)
	completed = models.DateTimeField('Completion Stamp', null=True, editable=False)
	
	class Meta:
		ordering = ('priority', 'created')
		
	def age(self):
		return datetime.now() - self.created
		
	def save(self):
		if not self.created:
			self.created = datetime.now()
			
		if self.complete:
			if self.completed == None:
				self.completed = datetime.now()
		else:
			self.completed = None
			
		super(Task, self).save()
	
	def __unicode__(self):
		return self.item+' ('+self.project.category.name+' => '+self.project.name+')'


class Thread(models.Model):
	content_type = models.ForeignKey(ContentType)
	content_object = generic.GenericForeignKey()
	object_id = models.PositiveIntegerField()
	creator = models.ForeignKey(User, editable=False)
	created = models.DateTimeField('Creation Stamp', editable=False)

	def save(self):
		if not self.created:
			self.created = datetime.now()

		super(Thread, self).save()
	
	def __unicode__(self):
		return self.content_object.__class__.__name__+' '+self.content_object.name


class Message(models.Model):
	thread = models.ForeignKey(Thread)
	text = models.TextField()
	creator = models.ForeignKey(User, editable=False, related_name='msg')
	created = models.DateTimeField('Creation Stamp', editable=False)
	
	class Meta:
		ordering = ('-created',)

	def save(self):
		if not self.created:
			self.created = datetime.now()

		super(Message, self).save()
	
	def __unicode__(self):
		return self.text

		
class Dependency(models.Model):
	task_a = models.ForeignKey(Task, related_name='depends_on')
	task_b = models.ForeignKey(Task, related_name='dependency_of')
	
	class Meta:
		verbose_name_plural = 'dependencies'
	
	def __unicode__(self):
		return self.task_a.__unicode__()+' ? '+self.task_b.__unicode__();
		

class UserAccount(models.Model):
	user = models.ForeignKey(User)
	account = models.ForeignKey(Account)
	
	def __unicode__(self):
		return self.user.username+':'+self.account.name
