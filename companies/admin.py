from django.contrib import admin
from .models import Company, JobPost


# ─── Inline: Show Jobs inside Company Admin ───────────────────────

class JobPostInline(admin.TabularInline):
    model  = JobPost
    extra  = 0
    fields = ['title', 'job_type', 'ctc_min', 'ctc_max', 'status', 'application_deadline']


# ─── Company Admin ────────────────────────────────────────────────

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display   = ('name', 'industry', 'location', 'is_active', 'created_at')
    list_filter    = ('industry', 'is_active')
    search_fields  = ('name', 'location')
    ordering       = ('name',)
    inlines        = [JobPostInline]


# ─── Job Post Admin ───────────────────────────────────────────────

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display  = (
        'title', 'company', 'job_type',
        'ctc_min', 'ctc_max', 'min_cgpa',
        'status', 'application_deadline'
    )
    list_filter   = ('status', 'job_type', 'company')
    search_fields = ('title', 'company__name')
    ordering      = ('-created_at',)