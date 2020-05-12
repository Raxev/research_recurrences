from django.urls import path

from . import views

app_name = "RecurrenceDemo"

urlpatterns = [
    path("", views.CourseList.as_view(), name="course_list"),
    path("detail/<int:id>/", views.DemoDetailView.as_view(), name="detail"),
    path("update/<int:id>/", views.DemoUpdateView.as_view(), name="update"),
    path("form/<int:id>/", views.DemoFormView.as_view(), name="form"),
]