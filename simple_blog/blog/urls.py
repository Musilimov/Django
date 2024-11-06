from django.urls import path,include
from . import views
urlpatterns = [
    path('listBlogs/', views.list_all,name="list_of_posts"),
    path('listBlogs/details/<int:id>/', views.single_post, name='details'),
    path('deletePost/<int:id>/', views.delete_post, name="delete_post"),
    path('editPost/<int:id>/', views.edit_post, name="edit_post"),
    path('createComment/<int:id>/', views.add_comment, name="create_comment"),
    path('edit/<int:id>/', views.edit_post, name='edit_post'),
]