from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView, DetailView
from django.utils import timezone
import json

from accounts.mixins import AdminRequiredMixin, StudentRequiredMixin
from students.models import StudentProfile

from .forms import InterviewScheduleForm
from .models import InterviewSchedule


# ════════════════════════════════════════════════
#  ADMIN VIEWS
# ════════════════════════════════════════════════

class InterviewListView(AdminRequiredMixin, ListView):
    model               = InterviewSchedule
    template_name       = 'interviews/interview_list.html'
    context_object_name = 'interviews'
    paginate_by         = 15

    def get_queryset(self):
        qs     = InterviewSchedule.objects.select_related(
                     'job__company'
                 ).prefetch_related('students').order_by(
                     'scheduled_date', 'start_time'
                 )
        status = self.request.GET.get('status')
        mode   = self.request.GET.get('mode')
        if status:
            qs = qs.filter(status=status)
        if mode:
            qs = qs.filter(mode=mode)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = InterviewSchedule.STATUS_CHOICES
        ctx['mode_choices']   = InterviewSchedule.MODE_CHOICES
        ctx['today']          = timezone.now().date()
        return ctx


class InterviewCreateView(AdminRequiredMixin, View):
    template_name = 'interviews/interview_form.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form':  InterviewScheduleForm(),
            'title': 'Schedule Interview'
        })

    def post(self, request):
        form = InterviewScheduleForm(request.POST)
        if form.is_valid():
            interview = form.save()
            messages.success(
                request,
                f'Interview scheduled for {interview.job.company.name} '
                f'on {interview.scheduled_date}.'
            )
            return redirect('interviews:interview_detail', pk=interview.pk)
        return render(request, self.template_name, {
            'form':  form,
            'title': 'Schedule Interview'
        })


class InterviewDetailView(AdminRequiredMixin, DetailView):
    model               = InterviewSchedule
    template_name       = 'interviews/interview_detail.html'
    context_object_name = 'interview'

    def get_queryset(self):
        return InterviewSchedule.objects.select_related(
            'job__company'
        ).prefetch_related('students__user')


class InterviewUpdateView(AdminRequiredMixin, View):
    template_name = 'interviews/interview_form.html'

    def get(self, request, pk):
        interview = get_object_or_404(InterviewSchedule, pk=pk)
        return render(request, self.template_name, {
            'form':      InterviewScheduleForm(instance=interview),
            'title':     'Edit Interview',
            'interview': interview,
        })

    def post(self, request, pk):
        interview = get_object_or_404(InterviewSchedule, pk=pk)
        form      = InterviewScheduleForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interview updated successfully.')
            return redirect('interviews:interview_detail', pk=pk)
        return render(request, self.template_name, {
            'form':      form,
            'title':     'Edit Interview',
            'interview': interview,
        })


class InterviewDeleteView(AdminRequiredMixin, View):

    def post(self, request, pk):
        interview = get_object_or_404(InterviewSchedule, pk=pk)
        company   = interview.job.company.name
        interview.delete()
        messages.success(request, f'Interview for {company} deleted.')
        return redirect('interviews:interview_list')


class CalendarView(AdminRequiredMixin, View):
    template_name = 'interviews/calendar.html'

    def get(self, request):
        interviews = InterviewSchedule.objects.select_related(
            'job__company'
        ).filter(status__in=['scheduled', 'postponed'])

        # ── Build calendar events for FullCalendar ──
        events = []
        color_map = {
            'aptitude':  '#1a56db',
            'technical': '#10b981',
            'hr':        '#f59e0b',
            'final':     '#8b5cf6',
            'gd':        '#ef4444',
        }
        for interview in interviews:
            events.append({
                'id':    interview.pk,
                'title': f"{interview.job.company.name} — {interview.get_round_name_display()}",
                'start': str(interview.scheduled_date) + 'T' + str(interview.start_time),
                'end':   str(interview.scheduled_date) + 'T' + str(interview.end_time) if interview.end_time else None,
                'color': color_map.get(interview.round_name, '#6b7280'),
                'url':   f'/interviews/{interview.pk}/',
                'extendedProps': {
                    'mode':    interview.get_mode_display(),
                    'venue':   interview.venue,
                    'students': interview.student_count,
                }
            })

        return render(request, self.template_name, {
            'events_json': json.dumps(events),
            'interviews':  interviews,
        })


# ════════════════════════════════════════════════
#  STUDENT VIEWS
# ════════════════════════════════════════════════

class MyInterviewsView(StudentRequiredMixin, View):
    template_name = 'interviews/my_interviews.html'

    def get(self, request):
        try:
            profile    = request.user.student_profile
            interviews = InterviewSchedule.objects.filter(
                students=profile
            ).select_related('job__company').order_by('scheduled_date', 'start_time')
        except StudentProfile.DoesNotExist:
            interviews = InterviewSchedule.objects.none()

        today    = timezone.now().date()
        upcoming = interviews.filter(scheduled_date__gte=today)
        past     = interviews.filter(scheduled_date__lt=today)

        return render(request, self.template_name, {
            'upcoming':   upcoming,
            'past':       past,
            'today':      today,
        })