from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View

from accounts.mixins import AdminRequiredMixin, StudentRequiredMixin
from companies.models import JobPost
from students.models import StudentProfile

from .forms import ApplicationStatusForm
from .models import Application, ApplicationStatusLog


# ════════════════════════════════════════════════
#  STUDENT VIEWS
# ════════════════════════════════════════════════

class ApplyJobView(StudentRequiredMixin, View):

    def post(self, request, job_pk):
        job = get_object_or_404(JobPost, pk=job_pk, status='open')

        try:
            profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            messages.error(request, 'Please create your profile first.')
            return redirect('students:create_profile')

        # ── Eligibility Checks ──────────────────
        if float(profile.cgpa) < float(job.min_cgpa):
            messages.error(request, 'You do not meet the CGPA requirement.')
            return redirect('companies:job_detail', pk=job_pk)

        if profile.backlogs > job.max_backlogs:
            messages.error(request, 'You exceed the allowed backlogs.')
            return redirect('companies:job_detail', pk=job_pk)

        if profile.branch not in job.eligible_branches:
            messages.error(request, 'Your branch is not eligible.')
            return redirect('companies:job_detail', pk=job_pk)

        if profile.year not in job.eligible_years:
            messages.error(request, 'Your year is not eligible.')
            return redirect('companies:job_detail', pk=job_pk)

        # ── Duplicate Check ─────────────────────
        if Application.objects.filter(student=profile, job=job).exists():
            messages.warning(request, 'You have already applied for this job.')
            return redirect('applications:my_applications')

        # ── Create Application ──────────────────
        application = Application.objects.create(student=profile, job=job)
        ApplicationStatusLog.objects.create(
            application=application,
            changed_to='applied',
            round_name='applied',
            remarks='Application submitted successfully.'
        )
        messages.success(request, f'Successfully applied for {job.title} at {job.company.name}!')
        return redirect('applications:my_applications')


class MyApplicationsView(StudentRequiredMixin, ListView):
    model               = Application
    template_name       = 'applications/my_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        try:
            profile = self.request.user.student_profile
            return Application.objects.filter(
                student=profile
            ).select_related('job__company').order_by('-applied_at')
        except StudentProfile.DoesNotExist:
            return Application.objects.none()


class ApplicationDetailStudentView(StudentRequiredMixin, DetailView):
    model               = Application
    template_name       = 'applications/application_detail_student.html'
    context_object_name = 'application'

    def get_queryset(self):
        try:
            profile = self.request.user.student_profile
            return Application.objects.filter(
                student=profile
            ).select_related('job__company').prefetch_related('status_logs')
        except StudentProfile.DoesNotExist:
            return Application.objects.none()


# ════════════════════════════════════════════════
#  ADMIN VIEWS
# ════════════════════════════════════════════════

class AllApplicationsView(AdminRequiredMixin, ListView):
    model               = Application
    template_name       = 'applications/all_applications.html'
    context_object_name = 'applications'
    paginate_by         = 20

    def get_queryset(self):
        qs     = Application.objects.select_related(
                     'student__user', 'job__company'
                 ).order_by('-applied_at')
        status = self.request.GET.get('status')
        job_id = self.request.GET.get('job')
        search = self.request.GET.get('search')
        if status:
            qs = qs.filter(status=status)
        if job_id:
            qs = qs.filter(job_id=job_id)
        if search:
            qs = qs.filter(
                Q(student__user__full_name__icontains=search) |
                Q(student__roll_number__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = Application.STATUS_CHOICES
        ctx['jobs'] = JobPost.objects.filter(
            applications__isnull=False
        ).distinct()
        return ctx


class ApplicationDetailAdminView(AdminRequiredMixin, DetailView):
    model               = Application
    template_name       = 'applications/application_detail_admin.html'
    context_object_name = 'application'

    def get_queryset(self):
        return Application.objects.select_related(
            'student__user', 'job__company'
        ).prefetch_related('status_logs')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ApplicationStatusForm(instance=self.object)
        return ctx


class UpdateApplicationStatusView(AdminRequiredMixin, View):

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        form        = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save()
            ApplicationStatusLog.objects.create(
                application=application,
                changed_to=application.status,
                round_name=application.current_round,
                remarks=form.cleaned_data.get('remarks', '')
            )
            # Auto-update placement status
            if application.status == 'selected':
                application.student.placement_status = 'placed'
                application.student.save()

            messages.success(request, 'Application status updated successfully.')
        return redirect('applications:application_detail_admin', pk=pk)


class JobApplicationsView(AdminRequiredMixin, ListView):
    model               = Application
    template_name       = 'applications/job_applications.html'
    context_object_name = 'applications'
    paginate_by         = 20

    def get_queryset(self):
        self.job = get_object_or_404(JobPost, pk=self.kwargs['job_pk'])
        qs = Application.objects.filter(
            job=self.job
        ).select_related('student__user').order_by('-applied_at')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['job']            = self.job
        ctx['status_choices'] = Application.STATUS_CHOICES
        base_qs = Application.objects.filter(job=self.job)
        ctx['stats'] = {
            'total':       base_qs.count(),
            'shortlisted': base_qs.filter(status='shortlisted').count(),
            'selected':    base_qs.filter(status='selected').count(),
            'rejected':    base_qs.filter(status='rejected').count(),
        }
        return ctx