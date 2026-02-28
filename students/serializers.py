from rest_framework import serializers
from .models import StudentProfile, AcademicRecord, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill_name', 'proficiency']


class AcademicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = ['id', 'exam_type', 'institution', 'board_university',
                  'year_of_passing', 'percentage_cgpa', 'semester_number']


class StudentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    academic_records = AcademicRecordSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'full_name', 'email', 'roll_number', 'branch', 'year',
            'section', 'cgpa', 'backlogs', 'phone', 'date_of_birth',
            'linkedin_url', 'github_url', 'placement_status',
            'resume', 'profile_photo', 'skills', 'academic_records',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['placement_status', 'created_at', 'updated_at']


class StudentProfileListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'full_name', 'email', 'roll_number',
                  'branch', 'year', 'cgpa', 'placement_status']