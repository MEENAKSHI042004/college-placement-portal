from django import forms
from .models import InterviewSchedule
from students.models import StudentProfile
from companies.models import JobPost


class InterviewScheduleForm(forms.ModelForm):

    students = forms.ModelMultipleChoiceField(
        queryset=StudentProfile.objects.select_related('user').all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Invite Students'
    )

    class Meta:
        model  = InterviewSchedule
        fields = [
            'job', 'round_name', 'mode',
            'scheduled_date', 'start_time', 'end_time',
            'venue', 'meeting_link', 'instructions',
            'status', 'students'
        ]
        widgets = {
            'job':            forms.Select(attrs={'class': 'form-select'}),
            'round_name':     forms.Select(attrs={'class': 'form-select'}),
            'mode':           forms.Select(attrs={'class': 'form-select'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time':     forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time':       forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Seminar Hall A'}),
            'meeting_link':   forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://meet.google.com/...'}),
            'instructions':   forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status':         forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show job as "Company — Title"
        self.fields['job'].queryset = JobPost.objects.select_related('company').all()
        self.fields['job'].label_from_instance = lambda obj: f"{obj.company.name} — {obj.title}"