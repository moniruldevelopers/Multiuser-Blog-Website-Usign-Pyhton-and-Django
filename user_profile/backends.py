from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from user_profile.models import User

class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, *args, **kwargs):
        try:
            # Use case-insensitive lookup for email
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
            else:
                return None

        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id: int):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except ObjectDoesNotExist:
            return None
