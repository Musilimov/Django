from django.shortcuts import render
from .models import Post,Comment
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotAllowed
from django.template import loader
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def list_all(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    else:
        form = PostForm()

    posts = Post.objects.all().values()
    template = loader.get_template('blog/post_list.html')
    context = {
        'myposts': posts,
        'form': form
    }

    return HttpResponse(template.render(context, request))

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