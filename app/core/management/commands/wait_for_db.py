import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Django command to wait for db."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                # Can this be done asynchronously with psycop3?
                # Also, what happens if the database never starts?
                # Maybe more complex
                self.stdout.write("Database unavailable, waiting 1 second.")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
