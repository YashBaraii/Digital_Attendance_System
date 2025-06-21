from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from classroom.models import Classroom
from attendance.models import Session, Attendance


# Test case for creating a classroom
class ClassCreationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            username="t11", password="pass123", role="teacher"
        )
        token_res = self.client.post(
            "/api/auth/token/", {"username": "t11", "password": "pass123"}
        )
        token = token_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_classroom(self):
        response = self.client.post(
            "/api/classrooms/", {"name": "Math 101111", "subject": "Mathematics"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
