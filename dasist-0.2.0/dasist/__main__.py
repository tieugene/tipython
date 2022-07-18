"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.management import execute_from_command_line

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
execute_from_command_line(sys.argv)
