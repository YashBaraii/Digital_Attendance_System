from django.contrib.auth.models import AbstractUser
from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ("teacher", "Teacher"),
        ("student", "Student"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
