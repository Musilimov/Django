from django.test import TestCase
from .models import Student
from users.models import User  # Поскольку User это кастомная модель, импортируем ее
from django.db.utils import IntegrityError


class StudentModelTest(TestCase):
    def setUp(self):
        """Setup a user and a student."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.student = Student.objects.create(
            user=self.user,
            name="John Doe",
            email="johndoe@example.com",
            dob="2000-01-01"
        )

    def test_student_creation(self):
        """Test the creation of a student record."""
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.email, "johndoe@example.com")
        self.assertEqual(str(self.student), "John Doe")

    def test_student_email_unique(self):
        """Test that a student's email is unique."""
        with self.assertRaises(IntegrityError):
            Student.objects.create(
                user=self.user,
                name="Jane Doe",
                email="johndoe@example.com",
                dob="2001-01-01"
            )

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Student
from django.test import TestCase

class StudentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="adminpassword")
        self.client.login(username="admin", password="adminpassword")
        self.student_data = {
            "user": self.user.id,
            "name": "John Doe",
            "email": "johndoe@example.com",
            "dob": "2000-01-01"
        }

    def test_create_student(self):
        """Test that a student can be created via the API."""
        url = reverse("student-list")  # Путь должен быть определен в urls.py вашего приложения
        response = self.client.post(url, self.student_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_student(self):
        """Test that a student's information can be updated via the API."""
        student = Student.objects.create(
            user=self.user,
            name="Old Name",
            email="oldemail@example.com",
            dob="1999-01-01"
        )
        url = reverse("student-detail", args=[student.id])  # Путь для детальной информации о студенте
        updated_data = {
            "name": "Updated Name",
            "email": "updatedemail@example.com",
            "dob": "1999-01-01"
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student.refresh_from_db()
        self.assertEqual(student.name, "Updated Name")

    def test_delete_student(self):
        """Test that a student can be deleted via the API."""
        student = Student.objects.create(
            user=self.user,
            name="John Doe",
            email="johndoe@example.com",
            dob="2000-01-01"
        )
        url = reverse("student-detail", args=[student.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(id=student.id)
