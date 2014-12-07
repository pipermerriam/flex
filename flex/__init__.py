import django
from django.conf import settings

if not settings.configured:
    settings.configure()
django.setup()

VERSION = '2.2.0'

from .core import load  # NOQA
