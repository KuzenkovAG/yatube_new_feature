from django.shortcuts import redirect
from django.urls import reverse_lazy


def post_owner_only(func):
    """Check post owner."""
    def check_owner(request, post_id, *args, **kwargs):
        author = request.user
        if author.posts.filter(id=post_id).exists():
            return func(request, post_id, *args, **kwargs)
        return redirect(reverse_lazy('posts:post_detail', args=[post_id]))
    return check_owner
