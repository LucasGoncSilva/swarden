from typing import Any, Literal
from os import system

from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--app",
            type=str,
            help='App to be covered - "." if nothing is defined.',
            default=".",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        omit_list: list[str] = [
            "*/month/*,",
            "*/migrations/*,",
            "manage.py,",
            "*/CORE/*,",
        ]

        app: Literal["."] | str = options["app"]

        system(
            f'coverage run --source=\'{app}\' --omit=\'{",".join(omit_list)}\' manage.py test {app}'
        )
        system("coverage html")

        self.stdout.write(self.style.SUCCESS("Coverage done + HTML file generated."))
