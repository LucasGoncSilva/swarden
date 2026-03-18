import subprocess
from typing import Any

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Runs tests with coverage using uv and generates an HTML report.'

    def handle(self, *args: Any, **options: Any) -> None:
        omit_patterns = [
            '*/month/*',
            '*/migrations/*',
            '*/admin.py',
            'manage.py',
            'server.py',
            '*/CORE/*',
        ]

        coverage_cmd = [
            'uv',
            'run',
            'coverage',
            'run',
            '--source=.',
            f'--omit={",".join(omit_patterns)}',
            'manage.py',
            'test',
        ]

        result = subprocess.run(coverage_cmd)

        self.stdout.write('Generating HTML report...')
        subprocess.run(['uv', 'run', 'coverage', 'html'])

        if result.returncode == 0:
            self.stdout.write(
                self.style.SUCCESS('Tests passed! Coverage HTML generated.')
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f'Tests failed with exit code {result.returncode}. '
                    'Check "htmlcov/index.html" for coverage of failed run.'
                )
            )
