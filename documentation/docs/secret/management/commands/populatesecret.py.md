
# File: `populatesecret.py`
Path: `SWARDEN.secret.management.commands`



---

## Imports

### `#!py import Any`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Any
    ```

### `#!py import User`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import User
    ```

### `#!py import BaseCommand`

Path: `#!py django.core.management`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.management import BaseCommand
    ```

### `#!py import Card`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import Card
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import SecurityNote
    ```

### `#!py import Month`

Path: `#!py secret.month.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.month.models import Month
    ```

### `#!py import tqdm`

Path: `#!py tqdm`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from tqdm import tqdm
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class Command`

Parents: `BaseCommand`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Command(BaseCommand):

        def handle(self, *args: Any, **options: Any) -> None:
            self.populate_cards()
            self.populate_notes()
            self.populate_credentials()

        def populate_cards(self) -> None:
            self.stdout.write('\nPopulating secret.Card')
            with open('./secret/management/commands/populate_card.txt') as sample:
                f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
            for i in tqdm(f, desc='Cards', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
                (owner, name, card_type, number, expiration, cvv, bank, brand, owners_name, note) = i
                owner: User = User.objects.get(pk=owner)
                (y, m) = expiration.split('-')
                expiration = Month(int(y), int(m))
                Card.objects.create(owner=owner, name=name, card_type=card_type, number=number, expiration=expiration, cvv=cvv, bank=bank, brand=brand, owners_name=owners_name, note=note, slug=f"{bank}{name.replace(' ', '-').lower()}")

        def populate_notes(self) -> None:
            self.stdout.write('\nPopulating secret.SecurityNote')
            with open('./secret/management/commands/populate_note.txt') as sample:
                f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
            for i in tqdm(f, desc='Notes', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
                (owner, title, note_type, content) = i
                owner = User.objects.get(pk=owner)
                SecurityNote.objects.create(owner=owner, title=title, note_type=note_type, content=content, slug=title.replace(' ', '-').lower())

        def populate_credentials(self) -> None:
            self.stdout.write('\nPopulating secret.LoginCredential')
            with open('./secret/management/commands/populate_credential.txt') as sample:
                f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
            for i in tqdm(f, desc='Notes', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
                (owner, service, name, thirdy_party_login, thirdy_party_login_name, login, password, note) = i
                owner = User.objects.get(pk=owner)
                LoginCredential.objects.create(owner=owner, service=service, name=name, thirdy_party_login=thirdy_party_login, thirdy_party_login_name=thirdy_party_login_name, login=login, password=password, note=note, slug=f"{service}{name.replace(' ', '-').lower()}")
    ```



---

## Functions

### `#!py def handle`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def handle(self, *args: Any, **options: Any) -> None:
        self.populate_cards()
        self.populate_notes()
        self.populate_credentials()
    ```

### `#!py def populate_cards`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def populate_cards(self) -> None:
        self.stdout.write('\nPopulating secret.Card')
        with open('./secret/management/commands/populate_card.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
        for i in tqdm(f, desc='Cards', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
            (owner, name, card_type, number, expiration, cvv, bank, brand, owners_name, note) = i
            owner: User = User.objects.get(pk=owner)
            (y, m) = expiration.split('-')
            expiration = Month(int(y), int(m))
            Card.objects.create(owner=owner, name=name, card_type=card_type, number=number, expiration=expiration, cvv=cvv, bank=bank, brand=brand, owners_name=owners_name, note=note, slug=f"{bank}{name.replace(' ', '-').lower()}")
    ```

### `#!py def populate_notes`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def populate_notes(self) -> None:
        self.stdout.write('\nPopulating secret.SecurityNote')
        with open('./secret/management/commands/populate_note.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
        for i in tqdm(f, desc='Notes', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
            (owner, title, note_type, content) = i
            owner = User.objects.get(pk=owner)
            SecurityNote.objects.create(owner=owner, title=title, note_type=note_type, content=content, slug=title.replace(' ', '-').lower())
    ```

### `#!py def populate_credentials`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def populate_credentials(self) -> None:
        self.stdout.write('\nPopulating secret.LoginCredential')
        with open('./secret/management/commands/populate_credential.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
        for i in tqdm(f, desc='Notes', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
            (owner, service, name, thirdy_party_login, thirdy_party_login_name, login, password, note) = i
            owner = User.objects.get(pk=owner)
            LoginCredential.objects.create(owner=owner, service=service, name=name, thirdy_party_login=thirdy_party_login, thirdy_party_login_name=thirdy_party_login_name, login=login, password=password, note=note, slug=f"{service}{name.replace(' ', '-').lower()}")
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
