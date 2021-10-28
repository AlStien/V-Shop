from django.contrib import admin
from django.urls import base, path, include

urlpatterns = [
    path('', include(base.urls)),
    path('admin/', admin.site.urls),
]
