from django.db import models
from django.contrib.auth.models import User

class APIRequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

class CourseMetrics(models.Model):
    course_name = models.CharField(max_length=255)
    views = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)
