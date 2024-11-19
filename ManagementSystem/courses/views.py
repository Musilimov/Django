from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view

from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework.filters import OrderingFilter
import django_filters

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from .models import Course
from .serializers import CourseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

import logging
from rest_framework.viewsets import ModelViewSet
from .models import Course
from .serializers import CourseSerializer

logger = logging.getLogger('custom')

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        logger.info(f"Course {course.name} created.")

    def enroll_student(self, student, course):
        logger.info(f"Student {student.name} enrolled in course {course.name}.")


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name']

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['name', 'instructor']  # Разрешаем сортировку по имени и преподавателю
    ordering = ['name']
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


@api_view(['GET'])  # Это должно быть списком строк
def get_courses(request):
    # Логика получения и кэширования курсов
    cached_courses = cache.get('courses_list')

    if cached_courses is not None:
        return Response(cached_courses)

    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)

    cache.set('courses_list', serializer.data, timeout=300)

    return Response(serializer.data)



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        # Кэшируем список курсов
        cached_courses = cache.get('courses_list')

        if cached_courses is not None:
            return Response(cached_courses)

        # Если в кэше нет данных, получаем их из базы данных
        response = super().list(request, *args, **kwargs)

        # Сохраняем в кэш с временем жизни 5 минут
        cache.set('courses_list', response.data, timeout=300)

        return response

