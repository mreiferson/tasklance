from django import forms
from models import *

class AccountForm(forms.ModelForm):
	class Meta:
		model = Account

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project

class TodoForm(forms.ModelForm):
	class Meta:
		model = Todo