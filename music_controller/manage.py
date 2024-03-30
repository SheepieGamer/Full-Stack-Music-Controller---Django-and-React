#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    Runs administrative tasks.

    This function sets the DJANGO_SETTINGS_MODULE environment variable to
    music_controller.settings, imports the django.core.management module, and
    then calls the execute_from_command_line function with the sys.argv list.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_controller.settings')
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
