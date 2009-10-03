from django import forms
from models import *

class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		exclude = ('created',)


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		exclude = ('created',)
		

class MilestoneForm(forms.ModelForm):
	class Meta:
		model = Milestone
		exclude = ('projects', 'created')


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		exclude = ('created',)


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		exclude = ('created', 'completed')


class LoadForm(forms.Form):
	file = forms.FileField()


class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		exclude = ('created',)