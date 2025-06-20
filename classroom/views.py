from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Classroom, Enrollment
from .serializers import ClassroomSerializer, EnrollmentSerializer
from users.permissions import IsTeacher, IsStudent

# List + Create Classes (Teacher)
class ClassroomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

# Update + Delete Class (Teacher only)
class ClassroomUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        # Restrict update/delete to teachers
        else:
            return [permissions.IsAuthenticated(), IsTeacher()]

# Student Enroll in Class
class EnrollInClassAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request, pk):
        try:
            classroom = Classroom.objects.get(pk=pk)
        except Classroom.DoesNotExist:
            return Response({"error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prevent duplicate enrollment
        if Enrollment.objects.filter(student=request.user, classroom=classroom).exists():
            return Response({"message": "Already enrolled."}, status=status.HTTP_400_BAD_REQUEST)

        enrollment = Enrollment.objects.create(student=request.user, classroom=classroom)
        return Response({"message": "Enrolled successfully."}, status=status.HTTP_201_CREATED)
