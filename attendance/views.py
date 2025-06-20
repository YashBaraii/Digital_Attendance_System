from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from classroom.models import Classroom
from .models import Session
from .serializers import SessionSerializer
from users.permissions import IsTeacher
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
