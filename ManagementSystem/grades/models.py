from django.conf import settings
from courses.models import Course
from django.db import models
class Grade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)  # Пример: A, B+, C
    date = models.DateField(auto_now_add=True)
    teacher = models.CharField(max_length=255)  # Это может быть ForeignKey на модель преподавателя

    def __str__(self):
        return f"{self.student.username} - {self.course.name}: {self.grade}"
