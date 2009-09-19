from django import forms
from models import *

class AccountForm(forms.ModelForm):
	class Meta:
		model = Account


class MilestoneForm(forms.ModelForm):
	class Meta:
		model = Milestone
		exclude = ('milestones',)


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task


class LoadForm(forms.Form):
	file = forms.FileField()


class MessageForm(forms.ModelForm):
	class Meta:
		model = Message