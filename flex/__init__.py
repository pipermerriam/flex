import django
from django.conf import settings

settings.configure()
django.setup()

VERSION = '1.1.0'

from .core import load  # NOQA
