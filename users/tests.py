from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from classroom.models import Classroom
from attendance.models import Session, Attendance


# Test cases for user registration functionality in the Digital Attendance System
class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_student_registration(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "student111",
                "email": "student@example.com",
                "password": "Test@123",
                "role": "student",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
