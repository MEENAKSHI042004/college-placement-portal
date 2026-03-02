from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


# ════════════════════════════════════════════════
#  HELPER
# ════════════════════════════════════════════════

def send_html_email(subject, template_name, context, recipient_email):
    """Send a styled HTML email with plain text fallback."""
    try:
        html_content  = render_to_string(template_name, context)
        plain_content = render_to_string(
            template_name.replace('.html', '_plain.txt'), context
        ) if False else ''   # plain fallback optional

        msg = EmailMultiAlternatives(
            subject    = subject,
            body       = f"Please view this email in an HTML-capable email client.",
            from_email = settings.DEFAULT_FROM_EMAIL,
            to         = [recipient_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


# ════════════════════════════════════════════════
#  EMAIL 1: Application Status Changed
# ════════════════════════════════════════════════

def send_status_change_email(application):
    """Send email when admin updates application status."""
    student_name  = application.student.user.full_name
    student_email = application.student.user.email
    job_title     = application.job.title
    company_name  = application.job.company.name
    new_status    = application.get_status_display()
    current_round = application.get_current_round_display()
    remarks       = application.remarks

    subject_map = {
        'shortlisted': f'🌟 You have been Shortlisted — {job_title} at {company_name}',
        'selected':    f'🎉 Congratulations! You are Selected — {job_title} at {company_name}',
        'rejected':    f'Application Update — {job_title} at {company_name}',
        'on_hold':     f'Application On Hold — {job_title} at {company_name}',
        'applied':     f'Application Received — {job_title} at {company_name}',
    }
    subject = subject_map.get(application.status, f'Application Update — {job_title}')

    context = {
        'student_name':  student_name,
        'job_title':     job_title,
        'company_name':  company_name,
        'new_status':    new_status,
        'current_round': current_round,
        'remarks':       remarks,
        'status_key':    application.status,
    }
    return send_html_email(
        subject        = subject,
        template_name  = 'emails/status_change.html',
        context        = context,
        recipient_email= student_email,
    )


# ════════════════════════════════════════════════
#  EMAIL 2: Application Submitted
# ════════════════════════════════════════════════

def send_application_confirmation_email(application):
    """Send confirmation when student applies."""
    context = {
        'student_name': application.student.user.full_name,
        'job_title':    application.job.title,
        'company_name': application.job.company.name,
        'deadline':     application.job.application_deadline,
        'ctc':          application.job.ctc_display,
    }
    return send_html_email(
        subject        = f'Application Submitted — {application.job.title} at {application.job.company.name}',
        template_name  = 'emails/application_confirmation.html',
        context        = context,
        recipient_email= application.student.user.email,
    )


# ════════════════════════════════════════════════
#  EMAIL 3: Welcome Email (New Student)
# ════════════════════════════════════════════════

def send_welcome_email(user, password):
    """Send welcome email when admin creates a student account."""
    context = {
        'student_name': user.full_name,
        'email':        user.email,
        'password':     password,
        'login_url':    'http://127.0.0.1:8000/accounts/login/',
    }
    return send_html_email(
        subject        = '🎓 Welcome to Placement Portal — Your Account Details',
        template_name  = 'emails/welcome.html',
        context        = context,
        recipient_email= user.email,
    )