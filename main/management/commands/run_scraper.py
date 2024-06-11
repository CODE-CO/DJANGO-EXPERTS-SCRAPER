import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run the scraper script'

    def handle(self, *args, **kwargs):
        subprocess.run(['python', 'scraper.py'])
