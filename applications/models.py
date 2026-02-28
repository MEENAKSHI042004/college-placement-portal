from django.db import models
from students.models import StudentProfile
from companies.models import JobPost


class Application(models.Model):

    STATUS_CHOICES = [
        ('applied',     'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected',    'Rejected'),
        ('selected',    'Selected'),
        ('on_hold',     'On Hold'),
    ]

    ROUND_CHOICES = [
        ('applied',   'Application Submitted'),
        ('aptitude',  'Aptitude Test'),
        ('technical', 'Technical Round'),
        ('hr',        'HR Round'),
        ('final',     'Final Round'),
        ('offer',     'Offer Released'),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='applications',
        db_index=True
    )
    job = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name='applications',
        db_index=True
    )
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied', db_index=True)
    current_round = models.CharField(max_length=20, choices=ROUND_CHOICES,  default='applied')
    applied_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    remarks       = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'job')
        ordering        = ['-applied_at']
        indexes = [
            models.Index(fields=['status', 'student']),
            models.Index(fields=['status', 'job']),
        ]

    def __str__(self):
        return f"{self.student.roll_number} → {self.job.title}"


class ApplicationStatusLog(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='status_logs'
    )
    changed_to = models.CharField(max_length=20)
    round_name = models.CharField(max_length=20, blank=True)
    remarks    = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.application} → {self.changed_to}"