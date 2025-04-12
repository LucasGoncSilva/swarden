from typing import Any

from account.models import User
from django.core.management import BaseCommand
from secret.models import Card, LoginCredential, SecurityNote
from secret.month.models import Month
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.populate_cards()
        self.populate_notes()
        self.populate_credentials()

    def populate_cards(self) -> None:
        if Card.objects.filter(slug='nao-listado--rdias').exists():
            self.stdout.write('secret.Card is already populated')
            return

        self.stdout.write('\nPopulating secret.Card')

        with open('./secret/management/commands/populatecard.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        for i in tqdm(f, desc='Cards', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
            (
                owner_id,
                name,
                card_type,
                number,
                expiration,
                cvv,
                bank,
                brand,
                owners_name,
                note,
            ) = i

            owner: User = User.objects.get(pk=owner_id)

            y, m = expiration.split('-')
            expiration = Month(int(y), int(m))

            Card.objects.create(
                owner=owner,
                name=name,
                card_type=card_type,
                number=number,
                expiration=expiration,
                cvv=cvv,
                bank=bank,
                brand=brand,
                owners_name=owners_name,
                note=note,
                slug=f'{bank}{name.replace(" ", "-").lower()}',
            )

    def populate_notes(self) -> None:
        if SecurityNote.objects.filter(slug='dolorem-mo').exists():
            self.stdout.write('secret.SecurityNote is already populated')
            return

        self.stdout.write('\nPopulating secret.SecurityNote')

        with open('./secret/management/commands/populatenote.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        for i in tqdm(f, desc='Notes', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
            owner_id, title, note_type, content = i

            owner = User.objects.get(pk=owner_id)

            SecurityNote.objects.create(
                owner=owner,
                title=title,
                note_type=note_type,
                content=content,
                slug=title.replace(' ', '-').lower(),
            )

    def populate_credentials(self) -> None:
        if LoginCredential.objects.filter(slug='discord--giovanna-cardoso').exists():
            self.stdout.write('secret.LoginCredential is already populated')
            return

        self.stdout.write('\nPopulating secret.LoginCredential')

        with open('./secret/management/commands/populatecredential.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        for i in tqdm(f, desc='Notes', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
            (
                owner_id,
                service,
                name,
                thirdy_party_login,
                thirdy_party_login_name,
                login,
                password,
                note,
            ) = i

            owner = User.objects.get(pk=owner_id)

            LoginCredential.objects.create(
                owner=owner,
                service=service,
                name=name,
                thirdy_party_login=thirdy_party_login,
                thirdy_party_login_name=thirdy_party_login_name,
                login=login,
                password=password,
                note=note,
                slug=f'{service}{name.replace(" ", "-").lower()}',
            )
