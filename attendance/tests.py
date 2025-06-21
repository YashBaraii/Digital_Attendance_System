from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from classroom.models import Classroom
from attendance.models import Session, Attendance


class QRCodeGenerationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            username="t2", password="pass123", role="teacher"
        )
        self.classroom = Classroom.objects.create(
            name="Physics", subject="Science", teacher=self.teacher
        )
        token_res = self.client.post(
            "/api/auth/token/", {"username": "t2", "password": "pass123"}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_res.data['access']}")

    def test_generate_qr(self):
        url = f"/api/attendance/classrooms/{self.classroom.id}/generate-session/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("qr_code_url", response.data)
