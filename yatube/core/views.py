from django.shortcuts import render
from django.views.generic import RedirectView
from django.urls import reverse_lazy


def bad_request(request, exception):
    return render(request, 'core/400.html', status=400)


def permission_denied(request, exception):
    return render(request, 'core/403.html', status=403)


def csrf_failure(request):
    return render(request, 'core/403csrf.html')


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'core/500.html', status=500)


class LastPageRedirectView(RedirectView):
    """Redirect on previous page."""
    http_method_names = ('get',)

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy(
            'posts:index')
