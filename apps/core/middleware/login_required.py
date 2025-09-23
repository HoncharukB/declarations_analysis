#NAMES
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import resolve

EXEMPT_URLS = [
    'welcome',
    'login',
    'logout',
    'logged_out',
    'register',
    'about',
    'admin:login',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver_match=resolve(request.path)
        view_name = resolver_match.view_name
        if view_name in EXEMPT_URLS:
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('welcome')

        return self.get_response(request)
        # raise PermissionDenied('You must be logged in to view this page.')

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            resolver_match=resolve(request.path)
            view_name = resolver_match.view_name
            if view_name == 'declarants_search' and request.user.role == 'guest':
                return redirect('welcome')
            elif view_name== 'declarants' and request.user.role == 'guest':
                return redirect('welcome')
            elif view_name == 'users':
                if request.user.role == 'user' or request.user.role == 'guest':
                    return redirect('welcome')
                elif request.user.role == 'admin':
                    return self.get_response(request)
        return self.get_response(request)