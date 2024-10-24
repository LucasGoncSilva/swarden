from random import choice
from typing import Any

from account.models import User
from django.core.management import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write('\nPopulating account.User')

        with open('./account/management/commands/populate_user.txt') as sample:
            lines: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        for i in tqdm(
            lines, desc='Users', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'
        ):
            username, email, password = i
            user: User = User.objects.create_user(
                username=username, email=email, password=password
            )

            if choice([True, False]):
                user.is_active = False

            user.save()
