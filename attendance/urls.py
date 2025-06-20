from django.urls import path
from .views import GenerateSessionQRView, MarkAttendanceView

urlpatterns = [
    path(
        "classrooms/<int:pk>/generate-session/",
        GenerateSessionQRView.as_view(),
        name="generate-session",
    ),
    path("mark/", MarkAttendanceView.as_view(), name="mark-attendance"),
]
