from typing import Any

from account.models import User
from alive_progress import alive_bar
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        if User.objects.filter(username='ernestodruso').exists():
            self.stdout.write(self.style.WARNING('\naccount.User is already populated'))
            return

        self.stdout.write('\nPopulating account.User')

        with open('./account/management/commands/populateuser.txt') as sample:
            lines: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        with alive_bar(len(lines), title='Users', bar='smooth', spinner='waves') as bar:
            for i in lines:
                username, passphrase = i

                user: User = User.objects.create_user(
                    username=username, password=passphrase
                )
                user.is_active = True  # type: ignore
                user.save()

                bar()
