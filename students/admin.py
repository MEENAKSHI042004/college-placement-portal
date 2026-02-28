from django.contrib import admin
from .models import StudentProfile, AcademicRecord, Skill


class AcademicRecordInline(admin.TabularInline):
    model = AcademicRecord
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'get_name', 'branch', 'year', 'cgpa', 'backlogs', 'placement_status')
    list_filter = ('branch', 'year', 'placement_status')
    search_fields = ('roll_number', 'user__full_name', 'user__email')
    inlines = [AcademicRecordInline, SkillInline]

    def get_name(self, obj):
        return obj.user.full_name
    get_name.short_description = 'Name'


@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam_type', 'institution', 'year_of_passing', 'percentage_cgpa')
    list_filter = ('exam_type',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill_name', 'proficiency')
    list_filter = ('proficiency',)