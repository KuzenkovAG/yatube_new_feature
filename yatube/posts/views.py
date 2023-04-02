from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.urls import reverse, reverse_lazy
from hitcount.views import HitCountDetailView

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post
from .utils import create_paginator, get_user_object

POST_LIMIT = settings.POST_LIMIT_ON_PAGE
User = get_user_model()


def post_owner_only(func):
    """Check post owner."""
    def check_owner(request, post_id, *args, **kwargs):
        author = request.user
        if author.posts.filter(id=post_id).exists():
            return func(request, post_id, *args, **kwargs)
        return redirect(reverse_lazy('posts:post_detail', args=[post_id]))
    return check_owner


@cache_page(2, key_prefix="index_page")
def index(request):
    """Main page."""
    template = 'posts/index.html'
    posts_list = Post.objects.select_related(
        'author', 'group', 'author__profile').prefetch_related(
        'comments', 'comments__author', 'user_likes', 'hit_count_generic').all()
    page_obj = create_paginator(request, posts_list, POST_LIMIT)
    return render(request, template, {'page_obj': page_obj})


def group_post(request, slug):
    """Page of group."""
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.select_related(
        'author', 'group', 'author__profile').prefetch_related(
        'comments', 'comments__author').all()
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
    posts = author.posts.select_related(
        'author', 'group', 'author__profile').prefetch_related(
        'comments', 'comments__author').all()
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


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    slug_field = 'post_id'
    count_hit = True

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')
        obj = get_object_or_404(
            Post.objects.select_related(
                'author', 'author__profile', 'group').prefetch_related(
                'comments', 'comments__author'
            ),
            id=post_id
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        post_count = self.object.author.posts.count()
        context['post_count'] = post_count
        context['form'] = form
        return context


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
    posts_list = Post.objects.select_related(
        'author', 'group', 'author__profile').prefetch_related(
        'comments', 'comments__author').filter(author__following__user=user)
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


@login_required
def like(request, post_id):
    """Add like on post."""
    if request.method == "GET":
        user = get_object_or_404(User, id=request.user.id)
        post = get_object_or_404(Post, id=post_id)
        if user not in post.user_likes.all():
            post.likes += 1
            post.user_likes.add(user)
            post.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike(request, post_id):
    """Remove like from post."""
    if request.method == "GET":
        user = get_object_or_404(User, id=request.user.id)
        post = get_object_or_404(Post, id=post_id)
        if user in post.user_likes.all():
            post.likes -= 1
            post.user_likes.remove(user)
            post.save()
    return redirect(request.META.get('HTTP_REFERER'))
