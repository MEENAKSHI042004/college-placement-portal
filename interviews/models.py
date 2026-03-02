from django.db import models
from students.models import StudentProfile
from companies.models import JobPost


class InterviewSchedule(models.Model):

    MODE_CHOICES = [
        ('online',   'Online'),
        ('offline',  'Offline'),
        ('hybrid',   'Hybrid'),
    ]

    ROUND_CHOICES = [
        ('aptitude',  'Aptitude Test'),
        ('technical', 'Technical Round'),
        ('hr',        'HR Round'),
        ('final',     'Final Round'),
        ('gd',        'Group Discussion'),
    ]

    STATUS_CHOICES = [
        ('scheduled',  'Scheduled'),
        ('completed',  'Completed'),
        ('cancelled',  'Cancelled'),
        ('postponed',  'Postponed'),
    ]

    job           = models.ForeignKey(
                        JobPost,
                        on_delete=models.CASCADE,
                        related_name='interviews'
                    )
    students      = models.ManyToManyField(
                        StudentProfile,
                        related_name='interviews',
                        blank=True
                    )
    round_name    = models.CharField(max_length=20, choices=ROUND_CHOICES)
    mode          = models.CharField(max_length=10, choices=MODE_CHOICES, default='offline')
    scheduled_date = models.DateField(db_index=True)
    start_time    = models.TimeField()
    end_time      = models.TimeField(null=True, blank=True)
    venue         = models.CharField(max_length=200, blank=True)
    meeting_link  = models.URLField(blank=True)
    instructions  = models.TextField(blank=True)
    status        = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_date', 'start_time']
        indexes  = [
            models.Index(fields=['scheduled_date', 'status']),
        ]

    def __str__(self):
        return f"{self.job.company.name} — {self.get_round_name_display()} — {self.scheduled_date}"

    @property
    def student_count(self):
        return self.students.count()