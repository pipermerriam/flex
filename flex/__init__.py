import django
from django.conf import settings

if not settings.configured:
    settings.configure()
django.setup()

VERSION = open('VERSION').read().strip()

from .core import load  # NOQA
