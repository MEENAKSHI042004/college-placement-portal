from django.urls import path
from . import views
from . import stats_views

app_name = 'accounts'

urlpatterns = [

    # ── Auth ──────────────────────────────────────
    path('login/',    views.LoginView.as_view(),  name='login'),
    path('logout/',   views.LogoutView.as_view(), name='logout'),

    # ── Dashboards ────────────────────────────────
    path('dashboard/',         views.DashboardView.as_view(),       name='dashboard'),
    path('dashboard/admin/',   views.AdminDashboardView.as_view(),   name='admin_dashboard'),
    path('dashboard/student/', views.StudentDashboardView.as_view(), name='student_dashboard'),

    # ── Stats ─────────────────────────────────────
    path('stats/',          stats_views.PlacementStatsView.as_view(), name='placement_stats'),
    path('stats/companies/',stats_views.CompanyStatsView.as_view(),   name='company_stats'),
    path('stats/students/', stats_views.StudentStatsView.as_view(),   name='student_stats'),
]