from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [

    # ── Admin URLs ─────────────────────────────────
    path('',
         views.InterviewListView.as_view(),
         name='interview_list'),

    path('create/',
         views.InterviewCreateView.as_view(),
         name='interview_create'),

    path('<int:pk>/',
         views.InterviewDetailView.as_view(),
         name='interview_detail'),

    path('<int:pk>/edit/',
         views.InterviewUpdateView.as_view(),
         name='interview_update'),

    path('<int:pk>/delete/',
         views.InterviewDeleteView.as_view(),
         name='interview_delete'),

    path('calendar/',
         views.CalendarView.as_view(),
         name='calendar'),

    # ── Student URLs ───────────────────────────────
    path('my/',
         views.MyInterviewsView.as_view(),
         name='my_interviews'),
]