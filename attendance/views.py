from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from classroom.models import Classroom
from .models import Session, Attendance
from .serializers import SessionSerializer, AttendanceSerializer
from users.permissions import IsTeacher, IsStudent
from .utils import generate_qr


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
