from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import CompanyViewSet, JobPostViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'jobs',      JobPostViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
]