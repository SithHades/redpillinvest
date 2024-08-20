from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('redpillinvest.api.urls')),
    path('api/v1/auth/', include('redpillinvest.authentication.urls')),
]