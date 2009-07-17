from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Account(models.Model):
	name = models.CharField(max_length=255)
	created = models.DateTimeField('Date Created', editable=False)
	
	def save(self):
		if self.created == None:
			self.created = datetime.now()
		super(Account, self).save()
	
	def __unicode__(self):
		return self.name


class Project(models.Model):
	account = models.ForeignKey(Account)
	name = models.CharField(max_length=255)
	created = models.DateTimeField('Date Created', editable=False)
	
	def save(self):
		if self.created == None:
			self.created = datetime.now()
		super(Project, self).save()
		
	def __unicode__(self):
		return self.name


class Category(models.Model):
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=255)
	created = models.DateTimeField('Date Created', editable=False)
	
	class Meta:
		verbose_name_plural = 'categories'
	
	def save(self):
		if self.created == None:
			self.created = datetime.now()
		super(Category, self).save()
	
	def __unicode__(self):
		return self.name+' ('+self.project.name+')'


class Todo(models.Model):
	category = models.ForeignKey(Category)
	item = models.CharField(max_length=255)
	complete = models.BooleanField(default=False)
	priority = models.PositiveIntegerField(default=0)
	created = models.DateTimeField('Creation Stamp', editable=False)
	completed = models.DateTimeField('Completion Stamp', null=True, editable=False)
	
	class Meta:
		ordering = ('priority',)
		
	def save(self):
		if self.created == None:
			self.created = datetime.now()
		super(Todo, self).save()
	
	def __unicode__(self):
		return self.item+' ('+self.category.project.name+' => '+self.category.name+')'

		
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