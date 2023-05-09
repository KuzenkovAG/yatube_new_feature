from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from hitcount.views import HitCountDetailView

from .decorators import post_owner_only
from .forms import CommentForm, PostForm
from .models import Follow, Group, Post
from .utils import get_user_object
from core.views import LastPageRedirectView

POST_LIMIT = settings.POST_LIMIT_ON_PAGE
User = get_user_model()


@method_decorator(cache_page(5), name='dispatch')
class IndexListView(ListView):
    """Index page."""
    template_name = 'posts/index.html'
    paginate_by = POST_LIMIT
    model = Post

    def get_queryset(self):
        queryset = self.model.objects.select_related(
            'author', 'group', 'author__profile').prefetch_related(
            'comments', 'comments__author', 'user_likes', 'hit_count_generic'
        ).all()
        return queryset


class GroupListView(ListView):
    """Page of group."""
    template_name = 'posts/group_list.html'
    paginate_by = POST_LIMIT
    model = Post

    def get_queryset(self):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        queryset = group.posts.select_related(
            'author', 'group', 'author__profile').prefetch_related(
            'comments', 'comments__author', 'user_likes', 'hit_count_generic'
        ).all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(
            Group,
            slug=self.kwargs.get('slug')
        )
        return context


class ProfileListView(ListView):
    """Page of Author."""
    template_name = 'posts/profile.html'
    paginate_by = POST_LIMIT
    model = Post

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = author.posts.select_related(
            'author', 'group', 'author__profile').prefetch_related(
            'comments', 'comments__author', 'user_likes', 'hit_count_generic'
        ).all()
        return queryset

    def get_context_data(self, object_list=None, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        context['author'] = author
        if self.request.user.is_authenticated:
            following = author.following.filter(user=self.request.user)
            context['following'] = following
        return context


class PostDetailView(HitCountDetailView):
    """Page of Post."""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    slug_field = 'post_id'
    count_hit = True

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            Post.objects.select_related(
                'author', 'author__profile', 'group').prefetch_related(
                'comments', 'comments__author'),
            id=self.kwargs.get('post_id')
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        post_count = self.object.author.posts.count()
        context['post_count'] = post_count
        context['form'] = form
        return context


@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    """Create new Comment to Post."""
    form_class = CommentForm

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.post_id = self.kwargs.get('post_id')
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse_lazy('posts:post_detail', args=[post_id])


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    """Create new Post."""
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:profile', args=[self.request.user.username])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать пост'
        return context


@method_decorator([login_required, post_owner_only], name='dispatch')
class PostUpdateView(UpdateView):
    """Update post content."""
    template_name = 'posts/create_post.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    model = Post

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'posts:post_detail',
            args=[self.kwargs.get('post_id')]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['title'] = 'Редактировать пост'
        return context


@method_decorator(login_required, name='dispatch')
class FollowsListView(ListView):
    """Page with posts of follows author."""
    template_name = 'posts/follow.html'
    paginate_by = POST_LIMIT
    model = Post

    def get_queryset(self):
        queryset = self.model.objects.select_related(
            'author', 'group', 'author__profile').prefetch_related(
            'comments', 'comments__author', 'user_likes', 'hit_count_generic'
        ).filter(author__following__user=self.request.user)
        return queryset


@method_decorator(login_required, name='dispatch')
class FollowRedirectView(LastPageRedirectView):
    """
    Follow to username.
    User can't follow yourself.
    If user already follow, don't create new one.
    """
    def get(self, request, *args, **kwargs):
        author = get_user_object(kwargs.get('username'))
        user = request.user
        follow = Follow.objects.filter(user=user, author=author).exists()
        if author != user and not follow:
            Follow.objects.create(user=user, author=author)
        return redirect(self.get_redirect_url(*args, **kwargs))


@method_decorator(login_required, name='dispatch')
class UnFollowRedirectView(LastPageRedirectView):
    """Unfollow from username."""
    def get(self, request, *args, **kwargs):
        author = get_user_object(kwargs.get('username'))
        Follow.objects.filter(user=request.user, author=author).delete()
        return redirect(self.get_redirect_url(*args, **kwargs))


@method_decorator(login_required, name='dispatch')
class LikeRedirectView(LastPageRedirectView):
    """Add like for post."""
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        if user not in post.user_likes.all():
            post.likes += 1
            post.user_likes.add(user)
            post.save()
        return redirect(self.get_redirect_url(*args, **kwargs))


@method_decorator(login_required, name='dispatch')
class DislikeRedirectView(LastPageRedirectView):
    """Remove like for post."""
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        if user in post.user_likes.all():
            post.likes -= 1
            post.user_likes.remove(user)
            post.save()
        return redirect(self.get_redirect_url(*args, **kwargs))
