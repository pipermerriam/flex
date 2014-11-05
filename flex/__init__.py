import django
from django.conf import settings

if not settings.configured:
    settings.configure()
django.setup()

VERSION = '1.9.0'

from .core import load  # NOQA
