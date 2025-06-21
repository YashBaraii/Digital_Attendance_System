from rest_framework import serializers
from .models import Classroom, Enrollment
from users.models import User


# Serializers for Classroom and Enrollment Models
class ClassroomSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source="teacher.username")

    class Meta:
        model = Classroom
        fields = ["id", "name", "subject", "teacher"]


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "classroom", "enrolled_at"]
        read_only_fields = ["student", "enrolled_at"]
