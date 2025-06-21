from django.contrib import admin
from .models import Attendance, Session

# Bonus Feature 3: Admin Interface for Attendance and Session Models


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "session", "status", "timestamp")
    list_filter = ("session__classroom", "student")
    search_fields = ("student__username", "session__classroom__name")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("classroom", "session_id", "date")
    list_filter = ("classroom", "date")
