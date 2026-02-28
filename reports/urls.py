from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [

    # ── Reports Home ──────────────────────────────────
    path('',
         views.ReportsHomeView.as_view(),
         name='reports_home'),

    # ── Individual Excel Downloads ────────────────────
    path('export/students/',
         views.ExportStudentsView.as_view(),
         name='export_students'),

    path('export/placed/',
         views.ExportPlacedStudentsView.as_view(),
         name='export_placed'),

    path('export/applications/',
         views.ExportApplicationsView.as_view(),
         name='export_applications'),

    path('export/branch-summary/',
         views.ExportBranchSummaryView.as_view(),
         name='export_branch_summary'),

    path('export/company-summary/',
         views.ExportCompanySummaryView.as_view(),
         name='export_company_summary'),

    # ── Full Multi-Sheet Report ───────────────────────
    path('export/full/',
         views.ExportFullReportView.as_view(),
         name='export_full'),
]