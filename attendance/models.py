import uuid
from django.db import models
from classroom.models import Classroom


class Session(models.Model):
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="sessions"
    )
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    date = models.DateField(auto_now_add=True)
    qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def __str__(self):
        return f"Session {self.session_id} for {self.classroom.name} on {self.date}"
