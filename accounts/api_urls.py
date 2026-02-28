from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import LoginAPIView, LogoutAPIView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('', include(router.urls)),
]