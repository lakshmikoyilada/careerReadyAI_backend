from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Simple health check endpoint for root path"""
    def get(self, request):
        return Response({"status": "ok", "message": "Server is running"})


urlpatterns = [
    path('', HealthCheckView.as_view(), name='health-check'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/careers/', include('apps.careers.urls')),
]
