from django.contrib import admin
from .models import Comment,Post
# Register your models here.
@admin.register(Comment)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('content','created_at','author')
    search_fields=('content','created_at','author')

@admin.register(Post)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('content','created_at','author')
    search_fields=('content','created_at','author')