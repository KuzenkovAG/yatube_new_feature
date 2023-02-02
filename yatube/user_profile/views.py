from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from posts.models import Follow

User = get_user_model()


class UserProfile(TemplateView):
    template_name = 'user_profile/profile.html'


class UserChangeDataView(UpdateView):
    """Page for registration of Users"""
    model = User
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('user_profile:index')
    template_name = 'users/signup.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class UserFollows(TemplateView):
    template_name = 'user_profile/follows.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['authors'] = user.follower.all()
        return context


class UserFollowers(TemplateView):
    template_name = 'user_profile/followers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['followers'] = user.following.all()
        followers = user.following.all()
        related_follows = {}
        for follower in followers:
            related_follows[follower] = Follow.objects.filter(
                user=user,
                author=follower.user,
            ).exists()
        context['related_follows'] = related_follows
        return context
