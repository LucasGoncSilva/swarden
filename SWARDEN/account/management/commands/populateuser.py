from typing import Any

from django.core.management import BaseCommand
from tqdm import tqdm

from account.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        print('\nPopulating account.User')

        with open('./account/management/commands/populate_user.txt', 'r') as sample:
            lines = [i.strip().split('::') for i in sample.readlines()]

        for i in tqdm(
            lines, desc='Users', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'
        ):
            username, email, password = i
            User.objects.create_user(username=username, email=email, password=password)
