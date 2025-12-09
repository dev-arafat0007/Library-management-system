from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class RedirectIfNotAuthenticated(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = ['/login', '/logout', '/signup']

        if not request.user.is_authenticated and request.path not in excluded_paths:
            return redirect('/login')
