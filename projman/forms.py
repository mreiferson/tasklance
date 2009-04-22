from django import forms
from models import *

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project

class TodoForm(forms.ModelForm):
	class Meta:
		model = Todo