from argparse import ArgumentParser

from django.core.management import BaseCommand
from main.data_migrations.data_migration import MigrationsRepository


class Command(BaseCommand):
    help = 'Run data migrations'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('migration_name', action='store',
                            help="Migration name to run (The file name without .py extension)")

    def handle(self, *args, **options):
        migration_name = options['migration_name']
        migration = MigrationsRepository.get(migration_name)
        try:
            self.stdout.write(f"Running migration ... ({migration.name})")
            migration.migrate()
            self.stdout.write("Migration done successfully!")
        except BaseException as e:
            print(e)
            self.stdout.write("Migration failed!")
            self.stdout.write("Rolling back migration ...")
            try:
                migration.rollback()
                self.stdout.write("Roll backed successfully.")
            except BaseException:
                print(e)
                self.stdout.write("The rollback also failed!")
