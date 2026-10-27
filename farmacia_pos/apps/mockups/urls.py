from django.urls import path

from . import views

app_name = "mockups"
urlpatterns = [
    path("", views.screen, name="inicio"),
    path("<slug:slug>/", views.screen, name="screen"),
]
