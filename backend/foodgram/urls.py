from django.contrib import admin
from django.urls import include, path


api_patterns = [
    path('', include('api.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('api/', include('rest_framework.urls'))
]
