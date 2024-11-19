"""
URL configuration for ManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from students.views import StudentViewSet


schema_view = get_swagger_view(title="ManagementSystem")
router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),  # Для базовой аутентификации через Djoser
    path('api/auth/', include('djoser.urls.jwt')),
    path('', include('users.urls')),
    path('api/students/', include('students.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/grades/', include('grades.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('swagger/', schema_view),
    *router.urls,
]
