from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdmin, IsStudent

from .models import AcademicRecord, Skill, StudentProfile
from .serializers import (AcademicRecordSerializer, SkillSerializer,
                           StudentProfileListSerializer, StudentProfileSerializer)


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user').prefetch_related(
        'skills', 'academic_records'
    ).order_by('-created_at')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__full_name', 'roll_number', 'branch']
    ordering_fields = ['cgpa', 'created_at', 'roll_number']

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentProfileListSerializer
        return StudentProfileSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update_status']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        branch = self.request.query_params.get('branch')
        year = self.request.query_params.get('year')
        status = self.request.query_params.get('status')
        min_cgpa = self.request.query_params.get('min_cgpa')
        if branch:
            qs = qs.filter(branch=branch)
        if year:
            qs = qs.filter(year=year)
        if status:
            qs = qs.filter(placement_status=status)
        if min_cgpa:
            qs = qs.filter(cgpa__gte=min_cgpa)
        return qs

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsStudent])
    def me(self, request):
        """Student views/updates their own profile."""
        try:
            profile = StudentProfile.objects.prefetch_related(
                'skills', 'academic_records'
            ).get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            return Response(StudentProfileSerializer(profile).data)

        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        profile = self.get_object()
        new_status = request.data.get('placement_status')
        if new_status not in dict(StudentProfile.STATUS_CHOICES):
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        profile.placement_status = new_status
        profile.save()
        return Response({'detail': 'Status updated.', 'placement_status': new_status})


class AcademicRecordViewSet(viewsets.ModelViewSet):
    serializer_class = AcademicRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return AcademicRecord.objects.select_related('student__user').all()
        try:
            profile = self.request.user.student_profile
            return AcademicRecord.objects.filter(student=profile)
        except StudentProfile.DoesNotExist:
            return AcademicRecord.objects.none()

    def perform_create(self, serializer):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        serializer.save(student=profile)


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Skill.objects.select_related('student__user').all()
        try:
            profile = self.request.user.student_profile
            return Skill.objects.filter(student=profile)
        except StudentProfile.DoesNotExist:
            return Skill.objects.none()

    def perform_create(self, serializer):
        from django.shortcuts import get_object_or_404
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        serializer.save(student=profile)