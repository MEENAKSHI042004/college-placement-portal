from django import forms
from students.models import StudentProfile
from .models import Company, JobPost


class CompanyForm(forms.ModelForm):
    class Meta:
        model  = Company
        fields = ['name', 'industry', 'website', 'description', 'logo', 'location', 'is_active']
        widgets = {
            'name':        forms.TextInput(attrs={'class': 'form-control'}),
            'industry':    forms.Select(attrs={'class': 'form-select'}),
            'website':     forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo':        forms.FileInput(attrs={'class': 'form-control'}),
            'location':    forms.TextInput(attrs={'class': 'form-control'}),
            'is_active':   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class JobPostForm(forms.ModelForm):

    eligible_branches = forms.MultipleChoiceField(
        choices=StudentProfile.BRANCH_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    eligible_years = forms.MultipleChoiceField(
        choices=StudentProfile.YEAR_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model  = JobPost
        fields = [
            'company', 'title', 'job_type',
            'description', 'responsibilities', 'requirements',
            'ctc_min', 'ctc_max', 'min_cgpa', 'max_backlogs',
            'eligible_branches', 'eligible_years',
            'application_deadline', 'drive_date',
            'status', 'location', 'vacancy_count'
        ]
        widgets = {
            'company':              forms.Select(attrs={'class': 'form-select'}),
            'title':                forms.TextInput(attrs={'class': 'form-control'}),
            'job_type':             forms.Select(attrs={'class': 'form-select'}),
            'description':          forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsibilities':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'requirements':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ctc_min':              forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ctc_max':              forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'min_cgpa':             forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_backlogs':         forms.NumberInput(attrs={'class': 'form-control'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'drive_date':           forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status':               forms.Select(attrs={'class': 'form-select'}),
            'location':             forms.TextInput(attrs={'class': 'form-control'}),
            'vacancy_count':        forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_eligible_branches(self):
        return list(self.cleaned_data.get('eligible_branches', []))

    def clean_eligible_years(self):
        return [int(y) for y in self.cleaned_data.get('eligible_years', [])]