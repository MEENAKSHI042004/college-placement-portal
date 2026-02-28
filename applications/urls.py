from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [

    # ── Student URLs ──────────────────────────────────────
    path(
        'apply/<int:job_pk>/',
        views.ApplyJobView.as_view(),
        name='apply_job'
    ),
    path(
        'my/',
        views.MyApplicationsView.as_view(),
        name='my_applications'
    ),
    path(
        'my/<int:pk>/',
        views.ApplicationDetailStudentView.as_view(),
        name='application_detail_student'
    ),

    # ── Admin URLs ────────────────────────────────────────
    path(
        'all/',
        views.AllApplicationsView.as_view(),
        name='all_applications'
    ),
    path(
        'all/<int:pk>/',
        views.ApplicationDetailAdminView.as_view(),
        name='application_detail_admin'
    ),
    path(
        'all/<int:pk>/update/',
        views.UpdateApplicationStatusView.as_view(),
        name='update_status'
    ),
    path(
        'job/<int:job_pk>/',
        views.JobApplicationsView.as_view(),
        name='job_applications'
    ),
]