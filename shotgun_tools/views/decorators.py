from django.utils.decorators import decorator_from_middleware
from shotgun_tools.middleware import ShotgunMiddleware

with_shotgun = decorator_from_middleware(ShotgunMiddleware)