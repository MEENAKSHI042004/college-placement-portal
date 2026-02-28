from rest_framework import serializers
from .models import Company, JobPost


class CompanySerializer(serializers.ModelSerializer):
    total_jobs = serializers.SerializerMethodField()

    class Meta:
        model  = Company
        fields = [
            'id', 'name', 'industry', 'website',
            'description', 'logo', 'location',
            'is_active', 'total_jobs', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_total_jobs(self, obj):
        return obj.job_posts.count()


class JobPostListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    ctc_display  = serializers.ReadOnlyField()

    class Meta:
        model  = JobPost
        fields = [
            'id', 'company_name', 'title', 'job_type',
            'ctc_display', 'min_cgpa', 'status',
            'application_deadline', 'location'
        ]


class JobPostSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    ctc_display  = serializers.ReadOnlyField()

    class Meta:
        model  = JobPost
        fields = [
            'id', 'company', 'company_name', 'title', 'job_type',
            'description', 'responsibilities', 'requirements',
            'ctc_min', 'ctc_max', 'ctc_display',
            'min_cgpa', 'max_backlogs',
            'eligible_branches', 'eligible_years',
            'application_deadline', 'drive_date',
            'status', 'location', 'vacancy_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']