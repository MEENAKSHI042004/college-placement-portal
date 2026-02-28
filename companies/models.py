from django.db import models


class Company(models.Model):

    INDUSTRY_CHOICES = [
        ('IT',            'Information Technology'),
        ('CORE',          'Core Engineering'),
        ('FINANCE',       'Finance & Banking'),
        ('CONSULTING',    'Consulting'),
        ('ECOMMERCE',     'E-Commerce'),
        ('HEALTHCARE',    'Healthcare'),
        ('EDUCATION',     'Education'),
        ('MANUFACTURING', 'Manufacturing'),
        ('OTHER',         'Other'),
    ]

    name        = models.CharField(max_length=200, unique=True, db_index=True)
    industry    = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, db_index=True)
    website     = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo        = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    location    = models.CharField(max_length=200, blank=True)
    is_active   = models.BooleanField(default=True, db_index=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']

    def __str__(self):
        return self.name


class JobPost(models.Model):

    JOB_TYPE_CHOICES = [
        ('full_time',  'Full Time'),
        ('internship', 'Internship'),
        ('contract',   'Contract'),
    ]

    STATUS_CHOICES = [
        ('open',     'Open'),
        ('closed',   'Closed'),
        ('upcoming', 'Upcoming'),
    ]

    company      = models.ForeignKey(
                       Company,
                       on_delete=models.CASCADE,
                       related_name='job_posts',
                       db_index=True
                   )
    title        = models.CharField(max_length=200, db_index=True)
    job_type     = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    description  = models.TextField()
    responsibilities = models.TextField(blank=True)
    requirements     = models.TextField(blank=True)

    # Package
    ctc_min = models.DecimalField(max_digits=10, decimal_places=2, help_text='LPA')
    ctc_max = models.DecimalField(max_digits=10, decimal_places=2, help_text='LPA')

    # Eligibility
    min_cgpa         = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, db_index=True)
    max_backlogs     = models.IntegerField(default=0)
    eligible_branches = models.JSONField(default=list)
    eligible_years    = models.JSONField(default=list)

    # Dates
    application_deadline = models.DateField(db_index=True)
    drive_date           = models.DateField(null=True, blank=True)

    # Status
    status        = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', db_index=True)
    location      = models.CharField(max_length=200, blank=True)
    vacancy_count = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'application_deadline']),
            models.Index(fields=['company', 'status']),
        ]

    def __str__(self):
        return f"{self.title} @ {self.company.name}"

    @property
    def ctc_display(self):
        return f"Rs.{self.ctc_min} - Rs.{self.ctc_max} LPA"