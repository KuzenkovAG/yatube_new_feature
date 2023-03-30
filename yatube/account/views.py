from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from posts.models import Follow
from account.models import Profile

User = get_user_model()


class UserAccount(TemplateView):
    template_name = 'account/index.html'


class UserChangeDataView(UpdateView):
    """Page for update user information."""
    model = User
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('account:index')
    template_name = 'account/update_user.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)


class AccountChangeDataView(UpdateView):
    """Page for update account information."""
    model = Profile
    fields = ('photo', 'bio', 'location', 'birth_date')
    success_url = reverse_lazy('account:index')
    template_name = 'account/update_user.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.profile.pk)


class UserFollows(TemplateView):
    """Show user what follows on you."""
    template_name = 'account/follows.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['authors'] = user.follower.all()
        return context


class UserFollowers(TemplateView):
    """Show your followers."""
    template_name = 'account/followers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['followers'] = user.following.all()
        related_follows = {}
        for follower in context['followers']:
            related_follows[follower] = Follow.objects.filter(
                user=user,
                author=follower.user,
            ).exists()
        context['related_follows'] = related_follows
        return context
