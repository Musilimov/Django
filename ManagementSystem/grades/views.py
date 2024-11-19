from rest_framework import viewsets, permissions
from .models import Grade
from .serializers import GradeSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser
import logging
from rest_framework.viewsets import ModelViewSet
from .models import Grade
from .serializers import GradeSerializer

logger = logging.getLogger('custom')

class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def perform_update(self, serializer):
        grade = serializer.save()
        logger.info(f"Grade updated: {grade.student.name} - {grade.course.name} = {grade.grade}.")
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
