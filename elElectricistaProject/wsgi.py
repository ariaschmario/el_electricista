"""
WSGI config for elElectricistaProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'elElectricistaProject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elElectricistaProject.settings')

application = get_wsgi_application()
