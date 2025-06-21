from django.contrib.auth.models import AbstractUser
from django.db import models


# Institution Model
# This model represents an educational institution such as a school or college.
class Institution(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# User Model
# This model extends the default Django user model to include a role and an optional institution.
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
