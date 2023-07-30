import functools

from django.http import HttpResponseForbidden


def forbidden_view(func):
    @functools.wraps(func)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return wrap
