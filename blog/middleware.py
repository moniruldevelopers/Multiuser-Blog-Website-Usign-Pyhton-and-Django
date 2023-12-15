from django.http import HttpResponseForbidden
from django.conf import settings
from .models import RestrictedEmail

class RestrictEmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is logged in
        if request.user.is_authenticated:
            user_email = request.user.email

            # Check if the user's email is in the list of restricted emails from the database
            if RestrictedEmail.objects.filter(email=user_email).exists():
                # Take appropriate action, e.g., deny access or redirect
                return HttpResponseForbidden("Access Forbidden")

        response = self.get_response(request)
        return response