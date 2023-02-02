from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.urls import reverse, reverse_lazy

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post
from .utils import create_paginator, get_user_object

POST_LIMIT = settings.POST_LIMIT_ON_PAGE


def post_owner_only(func):
    """Check post owner."""
    def check_owner(request, post_id, *args, **kwargs):
        author = request.user
        if author.posts.filter(id=post_id).exists():
            return func(request, post_id, *args, **kwargs)
        return redirect(reverse_lazy('posts:post_detail', args=[post_id]))
    return check_owner


@cache_page(1, key_prefix="index_page")
def index(request):
    """Main page."""
    template = 'posts/index.html'
    posts_list = Post.objects.select_related('author', 'group').all()
    page_obj = create_paginator(request, posts_list, POST_LIMIT)
    return render(request, template, {'page_obj': page_obj})


def group_post(request, slug):
    """Page of group."""
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    page_obj = create_paginator(request, posts_list, POST_LIMIT)

    template = 'posts/group_list.html'

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """Page of user profile."""
    author = get_user_object(username)
    posts = author.posts.all()
    post_count = posts.count()
    page_obj = create_paginator(request, posts, POST_LIMIT)
    username = request.user.username
    following = author.following.filter(user__username=username).exists()

    context = {
        'page_obj': page_obj,
        'post_count': post_count,
        'author': author,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Page of post detail."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    post_count = post.author.posts.count()
    comments = post.comments.all()

    context = {
        'post': post,
        'post_count': post_count,
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.post_id = post_id
        form.save()
    return redirect(reverse_lazy('posts:post_detail', args=[post_id]))


@login_required
def post_create(request):
    """Page for create new post."""
    title = 'Новый пост'
    form = PostForm(request.POST or None, files=request.FILES or None)
    template = 'posts/create_post.html'
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            form = form.save(commit=False)
            form.author = user
            form.save()
            return redirect(reverse_lazy(
                'posts:profile',
                args=[user.username]
            ))
    return render(request, template, {'form': form, 'title': title})


@login_required
@post_owner_only
def post_edit(request, post_id):
    """Page of edit post."""
    title = 'Редактировать пост'
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    template = 'posts/create_post.html'

    if request.method == 'POST':
        if form.is_valid():
            post.save()
            return redirect(reverse_lazy('posts:post_detail', args=[post_id]))
    return render(request, template, {
        'form': form,
        'title': title,
        'is_edit': True,
    })


@login_required
def follow_index(request):
    """Page show posts of the authors that the user is following."""
    user = request.user
    posts_list = Post.objects.filter(author__following__user=user)
    page_obj = create_paginator(request, posts_list, POST_LIMIT)
    return render(request, 'posts/follow.html', {'page_obj': page_obj})


@login_required
def profile_follow(request, username):
    """
    Follow to username.
    User can't follow yourself.
    If user already follow, don't create new one.
    """
    author = get_user_object(username)
    user = request.user
    follow = Follow.objects.filter(user=user, author=author).exists()
    if author != user and not follow:
        Follow.objects.create(user=user, author=author)
    return redirect(reverse('posts:profile', args=[username]))


@login_required
def profile_unfollow(request, username):
    """Unfollow from username."""
    author = get_user_object(username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect(reverse('posts:profile', args=[username]))
