from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdminOrReadOnly
from students.models import StudentProfile

from .models import Company, JobPost
from .serializers import CompanySerializer, JobPostListSerializer, JobPostSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset           = Company.objects.prefetch_related('job_posts').all()
    serializer_class   = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name', 'industry', 'location']
    ordering_fields    = ['name', 'created_at']

    def get_queryset(self):
        qs       = super().get_queryset()
        industry = self.request.query_params.get('industry')
        if industry:
            qs = qs.filter(industry=industry)
        return qs


class JobPostViewSet(viewsets.ModelViewSet):
    queryset           = JobPost.objects.select_related('company').order_by('-created_at')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['title', 'company__name', 'location']
    ordering_fields    = ['ctc_min', 'application_deadline', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return JobPostListSerializer
        return JobPostSerializer

    def get_queryset(self):
        qs       = super().get_queryset()
        status   = self.request.query_params.get('status')
        job_type = self.request.query_params.get('job_type')
        min_cgpa = self.request.query_params.get('min_cgpa')
        if status:
            qs = qs.filter(status=status)
        if job_type:
            qs = qs.filter(job_type=job_type)
        if min_cgpa:
            qs = qs.filter(min_cgpa__lte=min_cgpa)
        return qs

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def eligible(self, request):
        try:
            profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response(
                {'detail': 'Student profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        jobs = JobPost.objects.filter(
            status='open',
            min_cgpa__lte=profile.cgpa,
            max_backlogs__gte=profile.backlogs,
        ).select_related('company')

        jobs = [
            j for j in jobs
            if profile.branch in j.eligible_branches
            and profile.year  in j.eligible_years
        ]
        return Response(JobPostListSerializer(jobs, many=True).data)