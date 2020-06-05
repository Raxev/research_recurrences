"""API Url collection."""
from . import views
from django.urls import path, include


urlpatterns = [
    path("form_parser", views.ValidationAPIView.as_view(), name="parser"),
]
