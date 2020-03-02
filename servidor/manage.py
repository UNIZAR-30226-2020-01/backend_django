#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from utils.secret.set_credentials import the_secret_function

def main():
    if not os.getenv('TRAVIS', None):
        the_secret_function() # sets our top secret environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servidor.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
