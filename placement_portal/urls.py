from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',        admin.site.urls),
    path('accounts/',     include('accounts.urls')),
    path('students/',     include('students.urls')),
    path('companies/',    include('companies.urls')),
    path('applications/', include('applications.urls')),
    path('reports/',      include('reports.urls')),         # ← NEW
    path('api/v1/',       include('accounts.api_urls')),
    path('api/v1/',       include('students.api_urls')),
    path('api/v1/',       include('companies.api_urls')),
    path('api/v1/',       include('applications.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)