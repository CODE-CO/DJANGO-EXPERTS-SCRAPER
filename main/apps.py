import os
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from django.conf import settings
from django.core.management import call_command
import atexit
import threading
import time

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        if settings.SCHEDULER_AUTOSTART and os.environ.get('RUN_MAIN', None) != 'true':
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.run_scraper, 'interval', minutes=10)
            scheduler.start()
            # Delay the initial run to ensure the server has started
            threading.Thread(target=self.initial_run_scraper).start()
            # Shut down the scheduler when exiting the app
            atexit.register(lambda: scheduler.shutdown())

    def initial_run_scraper(self):
        time.sleep(5)  # Short delay to ensure the server starts
        self.run_scraper()

    @staticmethod
    def run_scraper():
        call_command('run_scraper')
