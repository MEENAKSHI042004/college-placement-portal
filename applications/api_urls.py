from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import ApplicationViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]