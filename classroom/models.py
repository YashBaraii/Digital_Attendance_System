from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Classroom Model
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="classrooms"
    )

    def __str__(self):
        return f"{self.name} - {self.subject}"


# Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "classroom")

    def __str__(self):
        return f"{self.student.username} enrolled in {self.classroom.name}"
