from django.contrib.auth import get_user_model


User = get_user_model()

class Backend(object):

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EmailPasswordBackend(Backend):

    def authenticate(self, username=None, password=None, **_kwargs):
        try:
            username=username.lower()
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user