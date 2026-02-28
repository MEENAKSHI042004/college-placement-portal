from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View

from accounts.mixins import AdminRequiredMixin, StudentRequiredMixin
from students.models import StudentProfile

from .forms import CompanyForm, JobPostForm
from .models import Company, JobPost


# ════════════════════════════════════════════════
#  COMPANY VIEWS — Admin Only
# ════════════════════════════════════════════════

class CompanyListView(AdminRequiredMixin, ListView):
    model               = Company
    template_name       = 'companies/company_list.html'
    context_object_name = 'companies'
    paginate_by         = 20

    def get_queryset(self):
        qs       = Company.objects.prefetch_related('job_posts').all()
        search   = self.request.GET.get('search')
        industry = self.request.GET.get('industry')
        if search:
            qs = qs.filter(name__icontains=search)
        if industry:
            qs = qs.filter(industry=industry)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['industry_choices'] = Company.INDUSTRY_CHOICES
        return ctx


class CompanyCreateView(AdminRequiredMixin, View):
    template_name = 'companies/company_form.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': CompanyForm(), 'title': 'Add Company'
        })

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company added successfully.')
            return redirect('companies:company_list')
        return render(request, self.template_name, {
            'form': form, 'title': 'Add Company'
        })


class CompanyUpdateView(AdminRequiredMixin, View):
    template_name = 'companies/company_form.html'

    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        return render(request, self.template_name, {
            'form': CompanyForm(instance=company), 'title': 'Edit Company'
        })

    def post(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        form    = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully.')
            return redirect('companies:company_list')
        return render(request, self.template_name, {
            'form': form, 'title': 'Edit Company'
        })


class CompanyDetailView(AdminRequiredMixin, DetailView):
    model               = Company
    template_name       = 'companies/company_detail.html'
    context_object_name = 'company'

    def get_queryset(self):
        return Company.objects.prefetch_related('job_posts')


# ════════════════════════════════════════════════
#  JOB POST VIEWS — Admin Only
# ════════════════════════════════════════════════

class JobPostListView(AdminRequiredMixin, ListView):
    model               = JobPost
    template_name       = 'companies/job_list.html'
    context_object_name = 'jobs'
    paginate_by         = 20

    def get_queryset(self):
        qs       = JobPost.objects.select_related('company').order_by('-created_at')
        status   = self.request.GET.get('status')
        job_type = self.request.GET.get('job_type')
        search   = self.request.GET.get('search')
        if status:
            qs = qs.filter(status=status)
        if job_type:
            qs = qs.filter(job_type=job_type)
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(company__name__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = JobPost.STATUS_CHOICES
        ctx['type_choices']   = JobPost.JOB_TYPE_CHOICES
        return ctx


class JobPostCreateView(AdminRequiredMixin, View):
    template_name = 'companies/job_form.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': JobPostForm(), 'title': 'Post a Job'
        })

    def post(self, request):
        form = JobPostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('companies:job_list')
        return render(request, self.template_name, {
            'form': form, 'title': 'Post a Job'
        })


class JobPostUpdateView(AdminRequiredMixin, View):
    template_name = 'companies/job_form.html'

    def get(self, request, pk):
        job  = get_object_or_404(JobPost, pk=pk)
        form = JobPostForm(instance=job)
        form.initial['eligible_branches'] = job.eligible_branches
        form.initial['eligible_years']    = [str(y) for y in job.eligible_years]
        return render(request, self.template_name, {
            'form': form, 'title': 'Edit Job'
        })

    def post(self, request, pk):
        job  = get_object_or_404(JobPost, pk=pk)
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('companies:job_list')
        return render(request, self.template_name, {
            'form': form, 'title': 'Edit Job'
        })


class JobPostDetailView(DetailView):
    model               = JobPost
    template_name       = 'companies/job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        return JobPost.objects.select_related('company')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.is_student:
            try:
                profile = self.request.user.student_profile
                job     = self.object
                ctx['is_eligible'] = (
                    float(profile.cgpa) >= float(job.min_cgpa) and
                    profile.backlogs    <= job.max_backlogs     and
                    profile.branch      in job.eligible_branches and
                    profile.year        in job.eligible_years
                )
            except StudentProfile.DoesNotExist:
                ctx['is_eligible'] = False
        return ctx


# ════════════════════════════════════════════════
#  JOB VIEWS — Student Only
# ════════════════════════════════════════════════

class StudentJobListView(StudentRequiredMixin, ListView):
    model               = JobPost
    template_name       = 'companies/student_job_list.html'
    context_object_name = 'jobs'
    paginate_by         = 20

    def get_queryset(self):
        qs       = JobPost.objects.select_related('company').filter(status='open').order_by('-created_at')
        job_type = self.request.GET.get('job_type')
        eligible = self.request.GET.get('eligible')
        if job_type:
            qs = qs.filter(job_type=job_type)
        if eligible:
            try:
                profile = self.request.user.student_profile
                qs = qs.filter(
                    min_cgpa__lte=profile.cgpa,
                    max_backlogs__gte=profile.backlogs
                )
            except StudentProfile.DoesNotExist:
                pass
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['type_choices'] = JobPost.JOB_TYPE_CHOICES
        try:
            ctx['profile'] = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            ctx['profile'] = None
        return ctx