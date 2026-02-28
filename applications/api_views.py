from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdmin, IsStudent
from companies.models import JobPost
from students.models import StudentProfile

from .models import Application, ApplicationStatusLog
from .serializers import (
    ApplicationListSerializer,
    ApplicationSerializer
)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related(
        'student__user', 'job__company'
    ).prefetch_related('status_logs').order_by('-applied_at')

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = [
        'student__user__full_name',
        'student__roll_number',
        'job__title'
    ]
    ordering_fields = ['applied_at', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        return ApplicationSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update_status']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs     = super().get_queryset()
        status = self.request.query_params.get('status')
        job_id = self.request.query_params.get('job')
        if status:
            qs = qs.filter(status=status)
        if job_id:
            qs = qs.filter(job_id=job_id)
        return qs

    @action(detail=False, methods=['get'], permission_classes=[IsStudent])
    def mine(self, request):
        """Student: view own applications."""
        try:
            profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        apps = Application.objects.filter(
            student=profile
        ).select_related('job__company').order_by('-applied_at')
        return Response(ApplicationListSerializer(apps, many=True).data)

    @action(detail=False, methods=['post'], permission_classes=[IsStudent])
    def apply(self, request):
        """Student: apply to a job."""
        job_id = request.data.get('job_id')
        if not job_id:
            return Response(
                {'error': 'job_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            job     = JobPost.objects.get(pk=job_id, status='open')
            profile = request.user.student_profile
        except JobPost.DoesNotExist:
            return Response(
                {'error': 'Job not found or closed.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except StudentProfile.DoesNotExist:
            return Response(
                {'error': 'Student profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if Application.objects.filter(student=profile, job=job).exists():
            return Response(
                {'error': 'Already applied.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application = Application.objects.create(student=profile, job=job)
        ApplicationStatusLog.objects.create(
            application=application,
            changed_to='applied',
            round_name='applied',
            remarks='Application submitted via API.'
        )
        return Response(
            ApplicationSerializer(application).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        """Admin: update application status."""
        application = self.get_object()
        new_status  = request.data.get('status')
        new_round   = request.data.get('current_round', application.current_round)
        remarks     = request.data.get('remarks', '')

        if new_status not in dict(Application.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status        = new_status
        application.current_round = new_round
        application.remarks       = remarks
        application.save()

        ApplicationStatusLog.objects.create(
            application=application,
            changed_to=new_status,
            round_name=new_round,
            remarks=remarks
        )

        if new_status == 'selected':
            application.student.placement_status = 'placed'
            application.student.save()

        return Response(ApplicationSerializer(application).data)