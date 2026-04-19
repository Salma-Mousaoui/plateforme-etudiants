from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authentication backend using email instead of username.
    Django uses 'username' by default — we override to use email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email__iexact=username).order_by("id").first()

        if user and user.check_password(password):
            return user  # is_active check handled by confirm_login_allowed
        return None
