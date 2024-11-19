from django.shortcuts import render
from .models import Post,Comment
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotAllowed
from django.template import loader
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

from django.db.models import Q  # Для создания сложных запросов

def list_all(request):
    query = request.GET.get('q')  # Получаем запрос поиска
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    else:
        form = PostForm()

    # Фильтрация постов по заголовку и содержимому
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        posts = Post.objects.all()

    # Пагинация для найденных постов
    paginator = Paginator(posts, 2)  # Указываем количество постов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'myposts': page_obj,
        'form': form,
        'page_obj': page_obj,
        'query': query,  # Добавляем запрос в контекст для отображения в шаблоне
    }

    return render(request, 'blog/post_list.html', context)


def single_post(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()  # Теперь это будет работать
    return render(request, 'blog/post_detail.html', {'mypost': post, 'comments': comments})

def new_post(request):
    if request.method == 'POST':
        form = PostForm(request)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        else:
            form = PostForm()

        template = loader.get_template('post_form.html')
        context = {'form': form}
        return HttpResponse(template.render(context, request))

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    # Проверяем, является ли текущий пользователь автором поста
    if post.author != request.user:
        messages.error(request, "У вас нет прав для редактирования этого поста.")
        return redirect('listBlogs')  # Перенаправляем на список постов

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно обновлён.')
            return redirect('details', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
def delete_post(request,post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        if post.author == request.user:
            post.delete()
        return redirect('post_form.html')
    return HttpResponseBadRequest("Invalid request method.")

def add_comment(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog/post_detail.html', id=id)
    else:
        form = CommentForm()

    template = loader.get_template('blog/post_form.html')
    context = {'form': form, 'post': post}
    return HttpResponse(template.render(context,request))

def list_comments(request):
    comments = Comment.objects.all()  # Получаем все комментарии из базы данных
    return render(request, 'blog/post_list.html', {'comments': comments})