#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from klym_telemetry.instrumenters import instrument_app


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    instrument_app(app_type='django', service_name="django", endpoint="http://collector:4317")
    instrument_app(app_type='psycopg2', service_name="database", endpoint="http://collector:4317")
    instrument_app(app_type='requests', service_name="requests", endpoint="http://collector:4317")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
