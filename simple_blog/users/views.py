from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm,ProfileForm
from .models import ProfileF,Follow
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            ProfileF.objects.create(user=user)

            messages.success(request, f'Account created for {username}. Your profile has been created.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/registration.html', {'form': form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(ProfileF, user=user)

    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    return render(request, 'users/profile.html', {
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })


@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == 'POST':
        bio = request.POST.get('bio', profile.bio)  # Получаем текущее био
        profile_picture = request.FILES.get('profile_picture')  # Получаем загруженное изображение

        profile.bio = bio  # Обновляем био
        if profile_picture:  # Если новое изображение загружено
            profile.profile_picture = profile_picture

        profile.save()  # Сохраняем профиль
        messages.success(request, 'Profile updated successfully!')  # Успешное сообщение
        return redirect('users/profile_view', username=request.user.username)

    return render(request, 'users/edit_profile.html', {'profile': profile})


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
    if follow:
        follow.delete()
    return redirect('profile', username=username)


def main(request):
    return render(request, 'users/main.html')


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f'You have successfully followed {user_to_follow.username}!')

    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    follow_relation = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
    if follow_relation.exists():
        follow_relation.delete()
        messages.success(request, f'You have successfully unfollowed {user_to_unfollow.username}.')

    return redirect('profile', username=username)

def add_picture(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('profile_view')
    else:
        form = ProfileForm()

    return render(request, 'users/profile.html', {'form': form})