from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from classroom.models import Classroom
from .models import Session, Attendance
from .serializers import SessionSerializer, AttendanceSerializer
from users.permissions import IsTeacher, IsStudent
from .utils import generate_qr
from users.models import User
from django.http import HttpResponse
import csv
from rest_framework.permissions import IsAdminUser
from django.db.models import Count


class GenerateSessionQRView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def post(self, request, pk):
        try:
            classroom = Classroom.objects.get(pk=pk, teacher=request.user)
        except Classroom.DoesNotExist:
            return Response(
                {"error": "Classroom not found or unauthorized."}, status=404
            )

        session = Session.objects.create(classroom=classroom)
        generate_qr(session)
        serializer = SessionSerializer(session, context={"request": request})
        return Response(serializer.data, status=201)


class MarkAttendanceView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        session_id = request.data.get("session_id")
        if not session_id:
            return Response({"error": "Session ID is required."}, status=400)

        try:
            session = Session.objects.get(session_id=session_id)
        except Session.DoesNotExist:
            return Response({"error": "Invalid session ID."}, status=404)

        # Prevent duplicate attendance
        if Attendance.objects.filter(student=request.user, session=session).exists():
            return Response({"message": "Attendance already marked."}, status=400)

        attendance = Attendance.objects.create(
            student=request.user, session=session, status="present"
        )
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=201)


# class StudentAttendanceSummaryView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, student_id):
#         try:
#             student = User.objects.get(id=student_id, role="student")
#         except User.DoesNotExist:
#             return Response({"error": "Student not found"}, status=404)

#         sessions = Session.objects.filter(classroom__enrollment__student=student)

#         # Optional date filtering
#         start_date = request.GET.get("start_date")
#         end_date = request.GET.get("end_date")

#         if start_date and end_date:
#             sessions = sessions.filter(date__range=[start_date, end_date])

#         total_sessions = sessions.count()
#         attended = Attendance.objects.filter(
#             student=student, session__in=sessions
#         ).count()

#         attended = Attendance.objects.filter(student=student).count()

#         attendance_percentage = (
#             (attended / total_sessions * 100) if total_sessions else 0
#         )
#         absences = total_sessions - attended

#         return Response(
#             {
#                 "student": student.username,
#                 "total_sessions": total_sessions,
#                 "attended": attended,
#                 "absences": absences,
#                 "attendance_percentage": f"{attendance_percentage:.2f}%",
#             }
#         )


# class ClassAttendanceSummaryView(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsTeacher]

#     def get(self, request, class_id):
#         try:
#             classroom = Classroom.objects.get(id=class_id, teacher=request.user)
#         except Classroom.DoesNotExist:
#             return Response({"error": "Class not found or unauthorized"}, status=404)

#         sessions = Session.objects.filter(classroom=classroom)

#         # Optional date filtering
#         start_date = request.GET.get("start_date")
#         end_date = request.GET.get("end_date")

#         if start_date and end_date:
#             sessions = sessions.filter(date__range=[start_date, end_date])

#         total_sessions = sessions.count()

#         enrolled_students = User.objects.filter(
#             enrollment__classroom=classroom, role="student"
#         )
#         student_summaries = []

#         for student in enrolled_students:
#             attended = Attendance.objects.filter(
#                 student=student, session__in=sessions
#             ).count()
#             percentage = (attended / total_sessions * 100) if total_sessions else 0
#             absences = total_sessions - attended
#             student_summaries.append(
#                 {
#                     "student": student.username,
#                     "attended": attended,
#                     "absences": absences,
#                     "attendance_percentage": f"{percentage:.2f}%",
#                 }
#             )

#         return Response(
#             {
#                 "class": classroom.name,
#                 "total_sessions": total_sessions,
#                 "students": student_summaries,
#             }
#         )


class StudentAttendanceSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, student_id):
        try:
            student = User.objects.get(id=student_id, role="student")
        except User.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

        sessions = Session.objects.filter(classroom__enrollment__student=student)

        # Optional: date filter
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if start_date and end_date:
            sessions = sessions.filter(date__range=[start_date, end_date])

        total_sessions = sessions.count()
        attended = Attendance.objects.filter(
            student=student, session__in=sessions
        ).count()

        if total_sessions == 0:
            absences = 0
            attendance_percentage = 0.00
        else:
            absences = max(total_sessions - attended, 0)
            attendance_percentage = (attended / total_sessions) * 100

        return Response(
            {
                "student": student.username,
                "total_sessions": total_sessions,
                "attended": attended,
                "absences": absences,
                "attendance_percentage": f"{attendance_percentage:.2f}%",
            }
        )


class ClassAttendanceSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request, class_id):
        try:
            classroom = Classroom.objects.get(id=class_id, teacher=request.user)
        except Classroom.DoesNotExist:
            return Response({"error": "Class not found or unauthorized"}, status=404)

        sessions = Session.objects.filter(classroom=classroom)

        # Optional: date filter
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if start_date and end_date:
            sessions = sessions.filter(date__range=[start_date, end_date])

        total_sessions = sessions.count()
        students = User.objects.filter(enrollment__classroom=classroom, role="student")

        student_summaries = []

        for student in students:
            attended = Attendance.objects.filter(
                student=student, session__in=sessions
            ).count()

            if total_sessions == 0:
                absences = 0
                percentage = 0.00
            else:
                absences = max(total_sessions - attended, 0)
                percentage = (attended / total_sessions) * 100

            student_summaries.append(
                {
                    "student": student.username,
                    "attended": attended,
                    "absences": absences,
                    "attendance_percentage": f"{percentage:.2f}%",
                }
            )

        return Response(
            {
                "class": classroom.name,
                "total_sessions": total_sessions,
                "students": student_summaries,
            }
        )


# Bonus Feature 2: CSV Export Endpoint
class ExportClassAttendanceCSV(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request, class_id):
        try:
            classroom = Classroom.objects.get(id=class_id, teacher=request.user)
        except Classroom.DoesNotExist:
            return Response({"error": "Class not found"}, status=404)

        sessions = Session.objects.filter(classroom=classroom)
        students = User.objects.filter(enrollment__classroom=classroom, role="student")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="{classroom.name}_attendance.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            ["Student", "Attended Sessions", "Total Sessions", "Attendance %"]
        )

        total_sessions = sessions.count()
        for student in students:
            attended = Attendance.objects.filter(
                student=student, session__in=sessions
            ).count()
            percent = (attended / total_sessions * 100) if total_sessions else 0
            writer.writerow(
                [student.username, attended, total_sessions, f"{percent:.2f}%"]
            )

        return response


# Bonus Feature 3: Dashboard Summary View - Custom Dashboard API


class DashboardSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_students = User.objects.filter(role="student").count()
        total_classes = Classroom.objects.count()
        total_attendances = Attendance.objects.count()

        # Top 5 most present students
        top_students = (
            Attendance.objects.values("student__username")
            .annotate(attended=Count("id"))
            .order_by("-attended")[:5]
        )

        # Top 5 most missed (students with lowest attendance)
        all_students = User.objects.filter(role="student")
        missed_data = []
        for student in all_students:
            attended = Attendance.objects.filter(student=student).count()
            missed_data.append({"student": student.username, "attended": attended})
        missed_data = sorted(missed_data, key=lambda x: x["attended"])[:5]

        return Response(
            {
                "total_students": total_students,
                "total_classes": total_classes,
                "total_attendance_records": total_attendances,
                "top_students": top_students,
                "least_attendance": missed_data,
            }
        )
