from django.db import models
from accounts.models import User


class StudentProfile(models.Model):

    BRANCH_CHOICES = [
        ('CSE',   'Computer Science & Engineering'),
        ('ECE',   'Electronics & Communication'),
        ('EEE',   'Cybersecurity '),
        ('MECH',  'Mechanical Engineering'),
        ('DS',  'Data Science'),
        ('AIML',  'AI & Machine Learning'),
    ]

    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]

    STATUS_CHOICES = [
        ('not_placed',     'Not Placed'),
        ('placed',         'Placed'),
        ('higher_studies', 'Higher Studies'),
    ]

    # ── Keep this alias so views work with both names ──
    PLACEMENT_STATUS_CHOICES = STATUS_CHOICES

    user        = models.OneToOneField(
                      User,
                      on_delete=models.CASCADE,
                      related_name='student_profile'
                  )
    roll_number = models.CharField(max_length=20, unique=True, db_index=True)
    branch      = models.CharField(max_length=10, choices=BRANCH_CHOICES, db_index=True)
    year        = models.IntegerField(choices=YEAR_CHOICES)
    section     = models.CharField(max_length=5, blank=True)
    cgpa        = models.DecimalField(max_digits=4, decimal_places=2, db_index=True)
    backlogs    = models.IntegerField(default=0)
    phone       = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address     = models.TextField(blank=True)
    resume      = models.FileField(upload_to='resumes/', null=True, blank=True)
    photo       = models.ImageField(upload_to='photos/', null=True, blank=True)
    linkedin    = models.URLField(blank=True)
    github      = models.URLField(blank=True)
    placement_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_placed',
        db_index=True
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['roll_number']
        indexes  = [
            models.Index(fields=['branch', 'placement_status']),
            models.Index(fields=['year', 'placement_status']),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.roll_number}"


class AcademicRecord(models.Model):

    EXAM_CHOICES = [
        ('10th',     '10th Standard'),
        ('12th',     '12th Standard'),
        ('diploma',  'Diploma'),
        ('semester', 'Semester'),
    ]

    student          = models.ForeignKey(
                           StudentProfile,
                           on_delete=models.CASCADE,
                           related_name='academic_records'
                       )
    exam_type        = models.CharField(max_length=20, choices=EXAM_CHOICES)
    institution      = models.CharField(max_length=200)
    board_university = models.CharField(max_length=200)
    year_of_passing  = models.IntegerField()
    percentage_cgpa  = models.DecimalField(max_digits=5, decimal_places=2)
    semester_number  = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['exam_type', 'semester_number']

    def __str__(self):
        return f"{self.student.roll_number} - {self.exam_type}"


class Skill(models.Model):

    PROFICIENCY_CHOICES = [
        ('beginner',     'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced',     'Advanced'),
    ]

    student     = models.ForeignKey(
                      StudentProfile,
                      on_delete=models.CASCADE,
                      related_name='skills'
                  )
    skill_name  = models.CharField(max_length=100)
    proficiency = models.CharField(
                      max_length=20,
                      choices=PROFICIENCY_CHOICES,
                      default='beginner'
                  )

    def __str__(self):
        return f"{self.student.roll_number} - {self.skill_name}"