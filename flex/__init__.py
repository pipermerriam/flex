import django
from django.conf import settings

settings.configure()
django.setup()

from .core import load  # NOQA
