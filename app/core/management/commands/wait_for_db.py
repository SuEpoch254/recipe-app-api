import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available.
    Go ahead when the db is available."""

    def handle(self, *args, **options):
        """Handle the command. A handle method is what is run whenever we
        run that command.
        Note: *args, **options) is to pass custom args and options to our
        management command"""
        # Print output to the screen to communicate with the user
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))