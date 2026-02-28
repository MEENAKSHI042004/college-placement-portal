from django import forms
from .models import Application


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ['status', 'current_round', 'remarks']
        widgets = {
            'status':        forms.Select(attrs={'class': 'form-select'}),
            'current_round': forms.Select(attrs={'class': 'form-select'}),
            'remarks':       forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }