from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [

    # ── Admin: Company Management ──────────────────────
    path('',              views.CompanyListView.as_view(),   name='company_list'),
    path('create/',       views.CompanyCreateView.as_view(), name='company_create'),
    path('<int:pk>/',     views.CompanyDetailView.as_view(), name='company_detail'),
    path('<int:pk>/edit/',views.CompanyUpdateView.as_view(), name='company_update'),

    # ── Admin: Job Management ──────────────────────────
    path('jobs/',                  views.JobPostListView.as_view(),   name='job_list'),
    path('jobs/create/',           views.JobPostCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/',         views.JobPostDetailView.as_view(), name='job_detail'),
    path('jobs/<int:pk>/edit/',    views.JobPostUpdateView.as_view(), name='job_update'),

    # ── Student: Browse Jobs ───────────────────────────
    path('browse/',  views.StudentJobListView.as_view(), name='browse_jobs'),
]