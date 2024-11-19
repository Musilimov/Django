from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view

from .models import Student
from .serializers import StudentSerializer

from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from rest_framework.response import Response
import logging
from rest_framework.viewsets import ModelViewSet
from .models import Student
from .serializers import StudentSerializer

logger = logging.getLogger('custom')

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @swagger_auto_schema(
        operation_description="Получить список студентов",
        responses={200: StudentSerializer(many=True)}
    )
    def perform_update(self, serializer):
        student = serializer.save()
        logger.info(f"Student {student.name}'s profile updated.")
    @swagger_auto_schema(
        operation_description="Создать нового студента",
        request_body=StudentSerializer,
        responses={201: StudentSerializer}
        )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])  # Параметр должен быть списком строк
def get_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

# Пример очистки кэша при изменении профиля студента
@api_view(['PUT'])
def update_student_profile(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    # Обновляем данные студента
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Инвалидируем кэш для этого студента
        cache.delete(f'student_profile_{student_id}')

        return Response(serializer.data)

    return Response(serializer.errors, status=400)
