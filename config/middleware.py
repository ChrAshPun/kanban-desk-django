from django.shortcuts import redirect
from django.urls import reverse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        if not request.user.is_authenticated and request.path != reverse('login'):
            return redirect('login')
        response = self.get_response(request)
        # Code to be executed for each request/response after the view is called.
        return response



