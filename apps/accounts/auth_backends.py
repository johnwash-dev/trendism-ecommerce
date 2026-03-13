from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailOTPBackend(ModelBackend):
    def authenticate(self, request, email=None, **kwargs):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
