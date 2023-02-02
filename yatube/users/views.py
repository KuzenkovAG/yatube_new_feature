from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, get_user_model
from django.shortcuts import get_object_or_404, redirect

from .forms import CreationForm

User = get_user_model()


class SignUp(CreateView):
    """Page for registration of Users"""
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        user = get_object_or_404(User, username=username)
        login(self.request, user)
        return redirect(self.success_url)
