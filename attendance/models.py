import uuid
from django.db import models
from classroom.models import Classroom
from users.models import User


class Session(models.Model):
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="sessions"
    )
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    date = models.DateField(auto_now_add=True)
    qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def __str__(self):
        return f"Session {self.session_id} for {self.classroom.name} on {self.date}"


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="present")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "session")  # prevent double attendance

    def __str__(self):
        return f"{self.student.username} → {self.session.classroom.name} @ {self.timestamp}"
