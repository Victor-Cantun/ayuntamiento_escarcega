from allauth.account.auth_backends import AuthenticationBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CustomAuthBackend(AuthenticationBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Buscar por email o username
        user = None
        if username:
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                try:
                    user = UserModel.objects.get(username=username)
                except UserModel.DoesNotExist:
                    return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
