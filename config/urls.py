"""
URL configuration for plateforme_etudiants project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Local apps
    path('', include('core.urls')),
    path('housing/', include('housing.urls')),
    path('', include('professionals.urls')),
    path('chat/', include('chat.urls')),
    path('reports/', include('reports.urls')),
    path('dashboard/', include('dashboard.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
