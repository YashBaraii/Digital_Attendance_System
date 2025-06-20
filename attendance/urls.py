from django.urls import path
from .views import (
    GenerateSessionQRView,
    MarkAttendanceView,
    StudentAttendanceSummaryView,
    ClassAttendanceSummaryView,
)

urlpatterns = [
    path(
        "classrooms/<int:pk>/generate-session/",
        GenerateSessionQRView.as_view(),
        name="generate-session",
    ),
    path("mark/", MarkAttendanceView.as_view(), name="mark-attendance"),
    path(
        "student/<int:student_id>/summary/",
        StudentAttendanceSummaryView.as_view(),
        name="student-summary",
    ),
    path(
        "class/<int:class_id>/summary/",
        ClassAttendanceSummaryView.as_view(),
        name="class-summary",
    ),
]
