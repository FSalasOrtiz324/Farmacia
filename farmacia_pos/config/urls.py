from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from apps.core.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
]

# Maquetas de interfaz con datos ficticios: nunca se publican fuera de desarrollo.
if settings.DEBUG:
    urlpatterns += [path("maquetas/", include("apps.mockups.urls"))]
