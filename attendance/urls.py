from django.urls import path
from .views import (
    GenerateSessionQRView,
    MarkAttendanceView,
    StudentAttendanceSummaryView,
    ClassAttendanceSummaryView,
    ExportClassAttendanceCSV,
    DashboardSummaryView,
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
    # Bonus Feature 2: Export Class Attendance as CSV
    path(
        "class/<int:class_id>/export/",
        ExportClassAttendanceCSV.as_view(),
        name="export-csv",
    ),
    # Bonus Feature 3: Dashboard Summary View
    path(
        "dashboard/summary/", DashboardSummaryView.as_view(), name="dashboard-summary"
    ),
]
