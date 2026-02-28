from django.db.models import Count, Q
from django.shortcuts import render

from accounts.mixins import AdminRequiredMixin
from applications.models import Application
from companies.models import Company, JobPost
from students.models import StudentProfile

from django.views.generic import View


class PlacementStatsView(AdminRequiredMixin, View):

    def get(self, request):

        # ════════════════════════════════════════
        #  OVERVIEW STATS
        # ════════════════════════════════════════
        total_students  = StudentProfile.objects.count()
        total_placed    = StudentProfile.objects.filter(placement_status='placed').count()
        total_unplaced  = StudentProfile.objects.filter(placement_status='not_placed').count()
        total_companies = Company.objects.filter(is_active=True).count()
        total_jobs      = JobPost.objects.count()
        total_apps      = Application.objects.count()

        placement_pct = round(
            (total_placed / total_students * 100) if total_students else 0, 1
        )

        # ════════════════════════════════════════
        #  BRANCH-WISE STATS
        # ════════════════════════════════════════
        branch_data = []
        for val, label in StudentProfile.BRANCH_CHOICES:
            total  = StudentProfile.objects.filter(branch=val).count()
            placed = StudentProfile.objects.filter(branch=val, placement_status='placed').count()
            pct    = round((placed / total * 100) if total else 0, 1)
            branch_data.append({
                'branch':  label,
                'total':   total,
                'placed':  placed,
                'pct':     pct,
            })

        # ════════════════════════════════════════
        #  YEAR-WISE STATS
        # ════════════════════════════════════════
        year_data = []
        for val, label in StudentProfile.YEAR_CHOICES:
            total  = StudentProfile.objects.filter(year=val).count()
            placed = StudentProfile.objects.filter(year=val, placement_status='placed').count()
            apps   = Application.objects.filter(student__year=val).count()
            pct    = round((placed / total * 100) if total else 0, 1)
            year_data.append({
                'year':   label,
                'total':  total,
                'placed': placed,
                'apps':   apps,
                'pct':    pct,
            })

        # ════════════════════════════════════════
        #  COMPANY-WISE STATS
        # ════════════════════════════════════════
        company_data = []
        for company in Company.objects.filter(is_active=True):
            total_apps_co  = Application.objects.filter(job__company=company).count()
            selected       = Application.objects.filter(
                                 job__company=company,
                                 status='selected'
                             ).count()
            open_jobs_co   = JobPost.objects.filter(
                                 company=company,
                                 status='open'
                             ).count()
            if total_apps_co > 0:
                company_data.append({
                    'name':      company.name,
                    'industry':  company.get_industry_display(),
                    'apps':      total_apps_co,
                    'selected':  selected,
                    'open_jobs': open_jobs_co,
                })

        company_data = sorted(company_data, key=lambda x: x['selected'], reverse=True)

        # ════════════════════════════════════════
        #  APPLICATION STATUS BREAKDOWN
        # ════════════════════════════════════════
        app_status_data = {
            'applied':     Application.objects.filter(status='applied').count(),
            'shortlisted': Application.objects.filter(status='shortlisted').count(),
            'selected':    Application.objects.filter(status='selected').count(),
            'rejected':    Application.objects.filter(status='rejected').count(),
            'on_hold':     Application.objects.filter(status='on_hold').count(),
        }

        # ════════════════════════════════════════
        #  TOP RECRUITERS
        # ════════════════════════════════════════
        top_recruiters = Application.objects.filter(
            status='selected'
        ).values(
            'job__company__name'
        ).annotate(
            selected_count=Count('id')
        ).order_by('-selected_count')[:5]

        context = {
            # Overview
            'total_students':  total_students,
            'total_placed':    total_placed,
            'total_unplaced':  total_unplaced,
            'total_companies': total_companies,
            'total_jobs':      total_jobs,
            'total_apps':      total_apps,
            'placement_pct':   placement_pct,
            # Breakdown
            'branch_data':     branch_data,
            'year_data':       year_data,
            'company_data':    company_data,
            'app_status_data': app_status_data,
            'top_recruiters':  top_recruiters,
        }
        return render(request, 'stats/placement_stats.html', context)


class CompanyStatsView(AdminRequiredMixin, View):

    def get(self, request):
        companies = Company.objects.filter(is_active=True)
        data = []
        for company in companies:
            jobs     = JobPost.objects.filter(company=company)
            apps     = Application.objects.filter(job__company=company)
            selected = apps.filter(status='selected').count()
            data.append({
                'company':   company,
                'jobs':      jobs.count(),
                'apps':      apps.count(),
                'selected':  selected,
                'open_jobs': jobs.filter(status='open').count(),
            })
        data = sorted(data, key=lambda x: x['apps'], reverse=True)
        return render(request, 'stats/company_stats.html', {'data': data})


class StudentStatsView(AdminRequiredMixin, View):

    def get(self, request):
        branch_filter = self.request.GET.get('branch')
        year_filter   = self.request.GET.get('year')

        students = StudentProfile.objects.select_related('user').prefetch_related('applications')

        if branch_filter:
            students = students.filter(branch=branch_filter)
        if year_filter:
            students = students.filter(year=year_filter)

        students = students.annotate(
            app_count=Count('applications')
        ).order_by('-app_count')

        context = {
            'students':       students,
            'branch_choices': StudentProfile.BRANCH_CHOICES,
            'year_choices':   StudentProfile.YEAR_CHOICES,
            'branch_filter':  branch_filter,
            'year_filter':    year_filter,
        }
        return render(request, 'stats/student_stats.html', context)