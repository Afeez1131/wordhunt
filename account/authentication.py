from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class GameParticipantsAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        return None

    def get_user(self, user_id):
        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)
            return user
        return None
