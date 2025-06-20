from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from classroom.models import Classroom
from .models import Session, Attendance
from .serializers import SessionSerializer, AttendanceSerializer
from users.permissions import IsTeacher, IsStudent
from .utils import generate_qr
from users.models import User


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
