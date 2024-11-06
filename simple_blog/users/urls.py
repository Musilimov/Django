from django.urls import path,include, re_path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/', views.profile_edit, name='edit_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('', views.main, name='main'),
    path('accounts/profile/<str:username>', views.profile_view, name='profile_view'),
    path('add_picture/', views.add_picture, name='add_picture')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]