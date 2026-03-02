from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [

    # ── Admin: Student Management ──────────────────
    path('',
         views.StudentListView.as_view(),
         name='student_list'),

    path('create/',
         views.AdminCreateStudentView.as_view(),
         name='create_student'),

    path('<int:pk>/',
         views.StudentDetailView.as_view(),
         name='student_detail'),

    path('<int:pk>/status/',
         views.UpdatePlacementStatusView.as_view(),
         name='update_placement_status'),

    # ── Admin: Bulk Upload ─────────────────────────
    path('bulk-upload/',
         views.BulkUploadView.as_view(),
         name='bulk_upload'),

    path('bulk-upload/sample/',
         views.DownloadSampleTemplateView.as_view(),
         name='download_sample'),

    # ── Student: Profile ───────────────────────────
    path('profile/',
         views.MyProfileView.as_view(),
         name='my_profile'),

    path('profile/create/',
         views.CreateProfileView.as_view(),
         name='create_profile'),

    path('profile/edit/',
         views.UpdateProfileView.as_view(),
         name='update_profile'),

    path('profile/academic/add/',
         views.AddAcademicRecordView.as_view(),
         name='add_academic'),

    path('profile/skill/add/',
         views.AddSkillView.as_view(),
         name='add_skill'),
]