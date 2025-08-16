# File: `populatesecret.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.secret.management.commands`

No file docstring provided.

---

## Imports

### `#!py import choices`

Path: `#!py random`

Category: native

??? example "Snippet"

    ```py
    from random import choices
    ```

### `#!py import Any`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Any
    ```

### `#!py import Self`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Self
    ```

### `#!py import User`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import User
    ```

### `#!py import BaseCommand`

Path: `#!py django.core.management`

Category: trdparty

??? example "Snippet"

    ```py
    from django.core.management import BaseCommand
    ```

### `#!py import slugify`

Path: `#!py django.utils.text`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.text import slugify
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import PaymentCard`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import PaymentCard
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import SecurityNote
    ```

### `#!py import Month`

Path: `#!py secret.month.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.month.models import Month
    ```

### `#!py import tqdm`

Path: `#!py tqdm`

Category: trdparty

??? example "Snippet"

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

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class Command(BaseCommand):

        def handle(self: Self, *args: Any, **options: Any) -> None:
            self.populate_cards()
            self.populate_notes()
            self.populate_credentials()

        def populate_cards(self: Self) -> None:
            if PaymentCard.objects.filter(slug='other--rdias').exists():
                self.stdout.write('secret.Card is already populated')
                return
            self.stdout.write('\nPopulating secret.Card')
            with open('./secret/management/commands/populatecard.txt') as sample:
                f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
            owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))
            for i, data in tqdm(enumerate(f), desc='Cards', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}', total=500):
                name, card_type, number, expiration, cvv, bank, brand, owners_name, note = data
                owner: User = User.objects.get(pk=owners_ids[i])
                y, m = expiration.split('-')
                expiration = Month(int(y), int(m))
                PaymentCard.objects.create(owner=owner, name=name, card_type=card_type, number=number, expiration=expiration, cvv=cvv, bank=bank, brand=brand, owners_name=owners_name, note=note, slug=f'{bank}{slugify(name)}')

        def populate_notes(self: Self) -> None:
            if SecurityNote.objects.filter(slug='dolorem-mo').exists():
                self.stdout.write('secret.SecurityNote is already populated')
                return
            self.stdout.write('\nPopulating secret.SecurityNote')
            with open('./secret/management/commands/populatenote.txt') as sample:
                f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
            owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))
            for i, data in tqdm(enumerate(f), desc='Payment Notes', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}', total=500):
                title, note_type, content = data
                owner = User.objects.get(pk=owners_ids[i])
                SecurityNote.objects.create(owner=owner, title=title, note_type=note_type, content=content, slug=slugify(title))

        def populate_credentials(self: Self) -> None:
            if LoginCredential.objects.filter(slug='discord--giovanna-cardoso').exists():
                self.stdout.write('secret.LoginCredential is already populated')
                return
            self.stdout.write('\nPopulating secret.LoginCredential')
            with open('./secret/management/commands/populatecredential.txt') as sample:
                f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
            owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))
            for i, data in tqdm(enumerate(f), desc='Login Credentials', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}', total=500):
                service, name, third_party_login, third_party_login_name, login, password, note = data
                owner = User.objects.get(pk=owners_ids[i])
                LoginCredential.objects.create(owner=owner, service=service, name=name, third_party_login=third_party_login, third_party_login_name=third_party_login_name, login=login, password=password, note=note, slug=f'{service}{slugify(name)}')
    ```



---

## Functions

### `#!py def handle`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def handle(self: Self, *args: Any, **options: Any) -> None:
        self.populate_cards()
        self.populate_notes()
        self.populate_credentials()
    ```

### `#!py def populate_cards`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def populate_cards(self: Self) -> None:
        if PaymentCard.objects.filter(slug='other--rdias').exists():
            self.stdout.write('secret.Card is already populated')
            return
        self.stdout.write('\nPopulating secret.Card')
        with open('./secret/management/commands/populatecard.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
        owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))
        for i, data in tqdm(enumerate(f), desc='Cards', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}', total=500):
            name, card_type, number, expiration, cvv, bank, brand, owners_name, note = data
            owner: User = User.objects.get(pk=owners_ids[i])
            y, m = expiration.split('-')
            expiration = Month(int(y), int(m))
            PaymentCard.objects.create(owner=owner, name=name, card_type=card_type, number=number, expiration=expiration, cvv=cvv, bank=bank, brand=brand, owners_name=owners_name, note=note, slug=f'{bank}{slugify(name)}')
    ```

### `#!py def populate_notes`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def populate_notes(self: Self) -> None:
        if SecurityNote.objects.filter(slug='dolorem-mo').exists():
            self.stdout.write('secret.SecurityNote is already populated')
            return
        self.stdout.write('\nPopulating secret.SecurityNote')
        with open('./secret/management/commands/populatenote.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
        owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))
        for i, data in tqdm(enumerate(f), desc='Payment Notes', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}', total=500):
            title, note_type, content = data
            owner = User.objects.get(pk=owners_ids[i])
            SecurityNote.objects.create(owner=owner, title=title, note_type=note_type, content=content, slug=slugify(title))
    ```

### `#!py def populate_credentials`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def populate_credentials(self: Self) -> None:
        if LoginCredential.objects.filter(slug='discord--giovanna-cardoso').exists():
            self.stdout.write('secret.LoginCredential is already populated')
            return
        self.stdout.write('\nPopulating secret.LoginCredential')
        with open('./secret/management/commands/populatecredential.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
        owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))
        for i, data in tqdm(enumerate(f), desc='Login Credentials', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}', total=500):
            service, name, third_party_login, third_party_login_name, login, password, note = data
            owner = User.objects.get(pk=owners_ids[i])
            LoginCredential.objects.create(owner=owner, service=service, name=name, third_party_login=third_party_login, third_party_login_name=third_party_login_name, login=login, password=password, note=note, slug=f'{service}{slugify(name)}')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
