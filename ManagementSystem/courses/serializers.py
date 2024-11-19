from rest_framework import serializers
from .models import Instructor, Course, Enrollment


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'bio']

class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer()  # Включаем информацию о преподавателе

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor']



class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # Отображение имени студента (или можно сделать более подробный сериализатор)
    course = CourseSerializer()  # Включаем информацию о курсе

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date', 'completion_date', 'status']