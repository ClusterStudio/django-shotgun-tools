from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

from utils import get_sg_connection


class ShotgunBackend(object):
    """
    Authenticate against Shotgun.

    Use the login name, and password.
    """
    @property
    def sg(self):
        if not hasattr(self, "_shotgun"):
            self._shotgun = get_sg_connection()
        return self._shotgun

    def authenticate(self, username=None, password=None):
        result = self.sg._connection.authenticate_human_user(username, password)
        if result:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password='get from shotgun')
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

