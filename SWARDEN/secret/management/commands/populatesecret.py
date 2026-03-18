from random import choices
from typing import Any

from account.models import User
from alive_progress import alive_bar
from crypt.algo import sWardenCryptography
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.text import slugify
from secret.models import (
    Bank,
    Brand,
    CardType,
    LoginCredential,
    NoteType,
    PaymentCard,
    SecurityNote,
    Service,
)
from secret.month.models import Month


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.warm()

        self.populate_card_types()
        self.populate_note_types()
        self.populate_banks()
        self.populate_brands()
        self.populate_services()

        self.populate_cards()
        self.populate_notes()
        self.populate_credentials()

    def warm(self) -> None:
        self.stdout.write('Warming up cryptography (Generating persistent cache)...\n')

        for i in (1, 2, 3, 4):
            self.stdout.write(f'\tWarming policy {i}... ')
            sWardenCryptography.encrypt(
                'imagine-its-a-super-strong-passphrase',
                settings.CRYPTOGRAPHY_KEY,
                settings.SYSTEM_PEPPER,
                i,
            )
            self.stdout.write('OK\n')

    def populate_note_types(self) -> None:
        if NoteType.objects.filter(name='Legal').exists():
            self.stdout.write(
                self.style.WARNING('secret.NoteType is already populated')
            )
            return

        self.stdout.write('\nPopulating secret.NoteType')

        data: list[NoteType] = [NoteType(name='Other')]

        with open('./secret/management/commands/pop_notetype.txt') as sample:
            f: set[str] = set(sample.readlines())

        with alive_bar(
            len(f), title='{:<15}'.format('NoteType'), bar='smooth', spinner='waves'
        ) as bar:
            for name in f:
                data.append(NoteType(name=name.strip()))

                bar()

        NoteType.objects.bulk_create(data, batch_size=500)

    def populate_card_types(self) -> None:
        if CardType.objects.filter(name='Co-branded').exists():
            self.stdout.write(
                self.style.WARNING('secret.CardType is already populated')
            )
            return

        self.stdout.write('\nPopulating secret.CardType')

        data: list[CardType] = [CardType(name='Other')]

        with open('./secret/management/commands/pop_cardtype.txt') as sample:
            f: set[str] = set(sample.readlines())

        with alive_bar(
            len(f), title='{:<15}'.format('CardType'), bar='smooth', spinner='waves'
        ) as bar:
            for name in f:
                data.append(CardType(name=name.strip()))

                bar()

        CardType.objects.bulk_create(data, batch_size=500)

    def populate_banks(self) -> None:
        if Bank.objects.filter(name='Zenith Bank').exists():
            self.stdout.write(self.style.WARNING('secret.Bank is already populated'))
            return

        self.stdout.write('\nPopulating secret.Bank')

        data: list[Bank] = [Bank(name='Other')]

        with open('./secret/management/commands/pop_bank.txt') as sample:
            f: set[str] = set(sample.readlines())

        with alive_bar(
            len(f), title='{:<15}'.format('Bank'), bar='smooth', spinner='waves'
        ) as bar:
            for name in f:
                data.append(Bank(name=name.strip()))

                bar()

        Bank.objects.bulk_create(data, batch_size=500)

    def populate_brands(self) -> None:
        if Brand.objects.filter(name='iDEAL').exists():
            self.stdout.write(self.style.WARNING('secret.Brand is already populated'))
            return

        self.stdout.write('\nPopulating secret.Brand')

        data: list[Brand] = [Brand(name='Other')]

        with open('./secret/management/commands/pop_brand.txt') as sample:
            f: set[str] = set(sample.readlines())

        with alive_bar(
            len(f), title='{:<15}'.format('Brand'), bar='smooth', spinner='waves'
        ) as bar:
            for name in f:
                data.append(Brand(name=name.strip()))

                bar()

        Brand.objects.bulk_create(data, batch_size=500)

    def populate_services(self) -> None:
        if Service.objects.filter(name='iDEAL').exists():
            self.stdout.write(self.style.WARNING('secret.Service is already populated'))
            return

        self.stdout.write('\nPopulating secret.Service')

        data: list[Service] = [Service(name='Other')]

        with open('./secret/management/commands/pop_service.txt') as sample:
            services: set[str] = set(sample.readlines())
        with open('./secret/management/commands/pop_bank.txt') as sample:
            banks: set[str] = set(sample.readlines())
        with open('./secret/management/commands/pop_brand.txt') as sample:
            brands: set[str] = set(sample.readlines())

        all_services: set[str] = set(services | banks | brands)

        with alive_bar(
            len(all_services),
            title='{:<15}'.format('Service'),
            bar='smooth',
            spinner='waves',
        ) as bar:
            for name in all_services:
                data.append(Service(name=name.strip()))

                bar()

        Service.objects.bulk_create(data, batch_size=500)

    def populate_cards(self) -> None:
        if PaymentCard.objects.filter(slug__icontains='andradetracy').exists():
            self.stdout.write(
                self.style.WARNING('secret.PaymentCard is already populated')
            )
            return

        self.stdout.write('\nPopulating secret.PaymentCard')

        with open('./secret/management/commands/pop_card.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        owners_ids: list[str] = choices(
            User.objects.values_list('id', flat=True), k=len(f)
        )
        cards_types_ids: list[str] = choices(
            CardType.objects.values_list('id', flat=True), k=len(f)
        )
        banks_ids_names: list[tuple[str, str]] = choices(
            Bank.objects.values_list('id', 'name'), k=len(f)
        )
        brands_ids: list[str] = choices(
            Brand.objects.values_list('id', flat=True), k=len(f)
        )

        data: list[PaymentCard] = []
        slugs: set[str] = set()

        with alive_bar(
            len(f), title='{:<15}'.format('PaymentCard'), bar='smooth', spinner='waves'
        ) as bar:
            for row in f:
                (
                    name,
                    number,
                    expiration,
                    branch,
                    account,
                    password,
                    cvv,
                    owners_name,
                    note,
                ) = row

                y, m = expiration.split('-')
                expiration: Month = Month(int(y), int(m))

                bank_id, bank_name = banks_ids_names.pop()

                slug: str = slugify(f'{bank_name} {name}')

                if slug in slugs:
                    continue

                data.append(
                    PaymentCard(
                        owner_id=owners_ids.pop(),
                        name=name,
                        card_type_id=cards_types_ids.pop(),
                        number=number,
                        expiration=expiration,
                        cvv=cvv,
                        bank_id=bank_id,
                        brand_id=brands_ids.pop(),
                        branch=branch,
                        account=account,
                        password=password,
                        owners_name=owners_name,
                        note=note,
                        slug=slug,
                    )
                )

                bar()

        PaymentCard.objects.bulk_create(data, batch_size=500)

    def populate_notes(self) -> None:
        if SecurityNote.objects.filter(slug='dolorem-mo').exists():
            self.stdout.write(
                self.style.WARNING('secret.SecurityNote is already populated')
            )
            return

        self.stdout.write('\nPopulating secret.SecurityNote')

        with open('./secret/management/commands/pop_note.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        owners_ids: list[str] = choices(
            User.objects.values_list('id', flat=True), k=len(f)
        )
        note_types_ids: list[str] = choices(
            NoteType.objects.values_list('id', flat=True), k=len(f)
        )

        data: list[SecurityNote] = []
        slugs: set[str] = set()

        with alive_bar(
            len(f), title='{:<15}'.format('SecurityNote'), bar='smooth', spinner='waves'
        ) as bar:
            for row in f:
                title, content = row
                slug = slugify(title)

                if slug in slugs:
                    continue

                data.append(
                    SecurityNote(
                        owner_id=owners_ids.pop(),
                        title=title,
                        note_type_id=note_types_ids.pop(),
                        content=content,
                        slug=slugify(title),
                    )
                )

                slugs.add(slug)

                bar()

        SecurityNote.objects.bulk_create(data, batch_size=500)

    def populate_credentials(self) -> None:
        if LoginCredential.objects.filter(slug__icontains='giovanna-cardoso').exists():
            self.stdout.write(
                self.style.WARNING('secret.LoginCredential is already populated')
            )
            return

        self.stdout.write('\nPopulating secret.LoginCredential')

        with open('./secret/management/commands/pop_credential.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        owners_ids: list[str] = choices(
            User.objects.values_list('id', flat=True), k=len(f)
        )
        services_ids_names: list[tuple[str, str]] = choices(
            Service.objects.values_list('id', 'name'), k=len(f)
        )

        data: list[LoginCredential] = []
        slugs: set[str] = set()

        with alive_bar(
            len(f),
            title='{:<15}'.format('LoginCredenial'),
            bar='smooth',
            spinner='waves',
        ) as bar:
            for row in f:
                (
                    name,
                    third_party_login,
                    third_party_login_name,
                    login,
                    password,
                    note,
                ) = row

                service_id, service_name = services_ids_names.pop()

                slug: str = slugify(f'{service_name} {name}')

                if slug in slugs:
                    continue

                data.append(
                    LoginCredential(
                        owner_id=owners_ids.pop(),
                        service_id=service_id,
                        name=name,
                        third_party_login=third_party_login,
                        third_party_login_name=third_party_login_name,
                        login=login,
                        password=password,
                        note=note,
                        slug=slug,
                    )
                )

                slugs.add(slug)

                bar()

        LoginCredential.objects.bulk_create(data, batch_size=500)
