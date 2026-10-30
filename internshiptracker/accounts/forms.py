from django import forms
from .models import Internship


class InternshipForm(forms.ModelForm):
	class Meta:
		model = Internship
		fields = ['company', 'role', 'status', 'date_applied', 'job_url', 'notes']
		widgets = {
			'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Northstar Labs'}),
			'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Product Design Intern'}),
			'status': forms.Select(attrs={'class': 'form-select'}),
			'date_applied': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'job_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
			'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a reminder or useful detail'}),
		}
