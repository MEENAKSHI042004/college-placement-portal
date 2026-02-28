from rest_framework import serializers
from .models import Application, ApplicationStatusLog


class StatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model        = ApplicationStatusLog
        fields       = ['id', 'changed_to', 'round_name', 'remarks', 'changed_at']
        read_only_fields = ['changed_at']


class ApplicationListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    roll_number  = serializers.CharField(source='student.roll_number',     read_only=True)
    job_title    = serializers.CharField(source='job.title',               read_only=True)
    company_name = serializers.CharField(source='job.company.name',        read_only=True)

    class Meta:
        model  = Application
        fields = [
            'id', 'student_name', 'roll_number',
            'job_title', 'company_name',
            'status', 'current_round', 'applied_at'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    roll_number  = serializers.CharField(source='student.roll_number',     read_only=True)
    job_title    = serializers.CharField(source='job.title',               read_only=True)
    company_name = serializers.CharField(source='job.company.name',        read_only=True)
    status_logs  = StatusLogSerializer(many=True, read_only=True)

    class Meta:
        model  = Application
        fields = [
            'id', 'student', 'student_name', 'roll_number',
            'job', 'job_title', 'company_name',
            'status', 'current_round', 'remarks',
            'status_logs', 'applied_at', 'updated_at'
        ]
        read_only_fields = ['applied_at', 'updated_at']