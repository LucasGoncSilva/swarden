# File: `populateuser.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.account.management.commands`

No file docstring provided.

---

## Imports

### `#!py import Any`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Any
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

        def handle(self, *args: Any, **options: Any) -> None:
            if User.objects.filter(username='ernestodruso').exists():
                self.stdout.write('\naccount.User is already populated')
                return
            self.stdout.write('\nPopulating account.User')
            with open('./account/management/commands/populateuser.txt') as sample:
                lines: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
            for i in tqdm(lines, desc='Users', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
                username, passphrase = i
                user: User = User.objects.create_user(username=username, password=passphrase)
                user.is_active = True
                user.save()
    ```



---

## Functions

### `#!py def handle`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def handle(self, *args: Any, **options: Any) -> None:
        if User.objects.filter(username='ernestodruso').exists():
            self.stdout.write('\naccount.User is already populated')
            return
        self.stdout.write('\nPopulating account.User')
        with open('./account/management/commands/populateuser.txt') as sample:
            lines: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
        for i in tqdm(lines, desc='Users', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
            username, passphrase = i
            user: User = User.objects.create_user(username=username, password=passphrase)
            user.is_active = True
            user.save()
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
