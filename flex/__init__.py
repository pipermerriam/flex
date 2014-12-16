import django
from django.conf import settings

if not settings.configured:
    settings.configure()
django.setup()

VERSION = '2.4.0'

from flex.core import load  # NOQA
