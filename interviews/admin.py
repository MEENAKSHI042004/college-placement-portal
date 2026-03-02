from django.contrib import admin
from .models import InterviewSchedule


@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):
    list_display  = (
        'get_company', 'round_name', 'mode',
        'scheduled_date', 'start_time', 'status', 'student_count'
    )
    list_filter   = ('status', 'mode', 'round_name', 'scheduled_date')
    search_fields = ('job__company__name', 'job__title')
    ordering      = ('scheduled_date', 'start_time')
    filter_horizontal = ('students',)

    def get_company(self, obj):
        return obj.job.company.name
    get_company.short_description = 'Company'