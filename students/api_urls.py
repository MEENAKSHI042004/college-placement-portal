from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import AcademicRecordViewSet, SkillViewSet, StudentProfileViewSet

router = DefaultRouter()
router.register(r'students', StudentProfileViewSet, basename='student')
router.register(r'academic-records', AcademicRecordViewSet, basename='academic')
router.register(r'skills', SkillViewSet, basename='skill')

urlpatterns = [
    path('', include(router.urls)),
]