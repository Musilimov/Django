from django.db import models
from users.models import User  # Импортируем кастомную модель пользователя

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
