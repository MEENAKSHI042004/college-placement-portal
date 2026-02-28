from django.contrib import admin
from .models import Application, ApplicationStatusLog


class StatusLogInline(admin.TabularInline):
    model           = ApplicationStatusLog
    extra           = 0
    fields          = ['changed_to', 'round_name', 'remarks', 'changed_at']
    readonly_fields = ['changed_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display  = (
        'get_student', 'get_job', 'get_company',
        'status', 'current_round', 'applied_at'
    )
    list_filter   = ('status', 'current_round')
    search_fields = (
        'student__roll_number',
        'student__user__full_name',
        'job__title'
    )
    ordering = ('-applied_at',)
    inlines  = [StatusLogInline]

    def get_student(self, obj):
        return obj.student.user.full_name
    get_student.short_description = 'Student'

    def get_job(self, obj):
        return obj.job.title
    get_job.short_description = 'Job'

    def get_company(self, obj):
        return obj.job.company.name
    get_company.short_description = 'Company'


@admin.register(ApplicationStatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('application', 'changed_to', 'round_name', 'changed_at')
    ordering     = ('-changed_at',)