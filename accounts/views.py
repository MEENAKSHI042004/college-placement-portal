from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import View

from accounts.mixins import AdminRequiredMixin, StudentRequiredMixin
from students.models import StudentProfile
from companies.models import JobPost, Company
from applications.models import Application


# ════════════════════════════════════════════════
#  AUTH VIEWS
# ════════════════════════════════════════════════

class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return render(request, self.template_name)

    def post(self, request):
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user     = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('accounts:dashboard')
        return render(request, self.template_name, {
            'error': 'Invalid email or password.'
        })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


# ════════════════════════════════════════════════
#  DASHBOARD VIEWS
# ════════════════════════════════════════════════

class DashboardView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.is_admin:
            return redirect('accounts:admin_dashboard')
        return redirect('accounts:student_dashboard')


class AdminDashboardView(AdminRequiredMixin, View):

    def get(self, request):
        # ── Core Stats ──────────────────────────
        total_students  = StudentProfile.objects.count()
        total_companies = Company.objects.filter(is_active=True).count()
        total_jobs      = JobPost.objects.filter(status='open').count()
        total_placed    = StudentProfile.objects.filter(placement_status='placed').count()
        total_apps      = Application.objects.count()

        placement_pct = round(
            (total_placed / total_students * 100) if total_students else 0, 1
        )

        # ── Recent Applications ──────────────────
        recent_apps = Application.objects.select_related(
            'student__user', 'job__company'
        ).order_by('-applied_at')[:5]

        # ── Recent Job Posts ─────────────────────
        recent_jobs = JobPost.objects.select_related(
            'company'
        ).order_by('-created_at')[:5]

        context = {
            'total_students':  total_students,
            'total_companies': total_companies,
            'total_jobs':      total_jobs,
            'total_placed':    total_placed,
            'total_apps':      total_apps,
            'placement_pct':   placement_pct,
            'recent_apps':     recent_apps,
            'recent_jobs':     recent_jobs,
        }
        return render(request, 'accounts/admin_dashboard.html', context)


class StudentDashboardView(StudentRequiredMixin, View):

    def get(self, request):
        try:
            profile = request.user.student_profile
            my_apps = Application.objects.filter(
                student=profile
            ).select_related('job__company').order_by('-applied_at')[:5]

            stats = {
                'total_applied':    Application.objects.filter(student=profile).count(),
                'shortlisted':      Application.objects.filter(student=profile, status='shortlisted').count(),
                'selected':         Application.objects.filter(student=profile, status='selected').count(),
                'rejected':         Application.objects.filter(student=profile, status='rejected').count(),
            }
            open_jobs = JobPost.objects.filter(
                status='open'
            ).select_related('company').order_by('-created_at')[:4]

        except StudentProfile.DoesNotExist:
            my_apps  = []
            stats    = {}
            open_jobs = JobPost.objects.filter(status='open')[:4]
            profile  = None

        return render(request, 'accounts/student_dashboard.html', {
            'profile':   profile,
            'my_apps':   my_apps,
            'stats':     stats,
            'open_jobs': open_jobs,
        })