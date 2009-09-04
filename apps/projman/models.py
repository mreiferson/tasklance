from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Account(models.Model):
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	subdomain = models.CharField(max_length=25)
	created = models.DateTimeField('Date Created', editable=False)
	
	def save(self):
		if self.created == None:
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

	def save(self):
		if self.created == None:
			self.created = datetime.now()
		super(Category, self).save()

	def __unicode__(self):
		return self.name+' ('+self.account.name+')'
		
		
class Milestone(models.Model):
	category = models.ForeignKey(Category)
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	deadline = models.DateTimeField()
	created = models.DateTimeField('Date Created', editable=False)
	priority = models.PositiveIntegerField(default=0)
	
	class Meta:
		ordering = ('priority', 'created')
	
	def save(self):
		if self.created == None:
			self.created = datetime.now()
		super(Milestone, self).save()
		
	def __unicode__(self):
		return self.name+' ('+self.category.name+')'


class Project(models.Model):
	account = models.ForeignKey(Category)
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	created = models.DateTimeField('Date Created', editable=False)
	priority = models.PositiveIntegerField(default=0)
	
	class Meta:
		ordering = ('priority', 'created')
	
	def save(self):
		if self.created == None:
			self.created = datetime.now()
		super(Project, self).save()
		
	def __unicode__(self):
		return self.name+' ('+self.category.name+')'


class Todo(models.Model):
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
		if self.created == None:
			self.created = datetime.now()
			
		if self.complete:
			if self.completed == None:
				self.completed = datetime.now()
		else:
			self.completed = None
			
		super(Todo, self).save()
	
	def __unicode__(self):
		return self.item+' ('+self.project.category.name+' => '+self.project.name+')'

		
class Dependency(models.Model):
	todo_a = models.ForeignKey(Todo, related_name='depends_on')
	todo_b = models.ForeignKey(Todo, related_name='dependency_of')
	
	class Meta:
		verbose_name_plural = 'dependencies'
	
	def __unicode__(self):
		return self.todo_a.__unicode__()+' ? '+self.todo_b.__unicode__();
		

class UserAccount(models.Model):
	user = models.ForeignKey(User)
	account = models.ForeignKey(Account)
	
	def __unicode__(self):
		return self.user.username+':'+self.account.name
