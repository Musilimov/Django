from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from users.models import User

class PermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username="admin", password="adminpassword")
        self.regular_user = User.objects.create_user(username="user", password="userpassword")
        self.student_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "dob": "2000-01-01"
        }

    def test_admin_can_create_student(self):
        """Test that an admin user can create a student."""
        self.client.login(username="admin", password="adminpassword")
        url = reverse("student-list")  # URL для списка студентов
        response = self.client.post(url, self.student_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_student(self):
        """Test that a regular user cannot create a student."""
        self.client.login(username="user", password="userpassword")
        url = reverse("student-list")  # URL для списка студентов
        response = self.client.post(url, self.student_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
