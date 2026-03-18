import subprocess
from pathlib import Path
from typing import Any, Final

from django.conf import settings
from django.core.management import BaseCommand, CommandParser
from django.db.migrations.loader import MigrationLoader


class Command(BaseCommand):
    help: str = 'Lists all migration files for the specified apps'

    OUTPUT_PATH: Final[Path] = settings.BASE_DIR / 'migrations.sql'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'app_names', nargs='+', type=str, help='Names of the Django apps'
        )

    def handle(self, *args: Any, **options: Any) -> None:
        loader: MigrationLoader = MigrationLoader(None, ignore_no_migrations=True)

        sql_list: list[str] = []

        for app_label in options['app_names']:
            self.stdout.write(self.style.MIGRATE_LABEL(f'App: {app_label}'))

            app_migrations: list[tuple[str, str]] = [
                m for m, _ in loader.disk_migrations.items() if m[0] == app_label
            ]

            if not app_migrations:
                self.stdout.write(
                    self.style.WARNING(f"  - No migrations found for '{app_label}'")
                )

                continue

            app_migrations.sort(key=lambda x: x[1])

            for app, migration in app_migrations:
                sql_list.append(self.get_migration_sql(app, migration).strip() + '\n\n')
                self.stdout.write(f'  {app}.{migration}: OK')

        with open(self.OUTPUT_PATH, 'w') as f:
            f.writelines(sql_list)

        self.stdout.write(self.style.SUCCESS(f'SQL generated: {self.OUTPUT_PATH}'))

    def get_migration_sql(self, app: str, migration: str) -> str:
        command: list[str] = [
            'uv',
            'run',
            'python',
            'manage.py',
            'sqlmigrate',
            app,
            migration,
        ]

        return subprocess.run(
            command, capture_output=True, text=True, check=True
        ).stdout
