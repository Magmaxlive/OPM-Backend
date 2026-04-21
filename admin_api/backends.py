# api/backends.py
from django.contrib.auth import get_user_model

class EmailOrUsernameBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            # Try email first
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Fall back to username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None