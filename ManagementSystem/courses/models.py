from django.db import models
from students.models import Student
from django.db import models
from users.models import User
class Instructor(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses")

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)  # Дата завершения курса
    status = models.CharField(max_length=20, default='active')  # Статус записи (например, 'active', 'completed')

    class Meta:
        unique_together = ('student', 'course')  # Убедимся, что студент не может записаться на один и тот же курс дважды

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name} ({self.status})"
