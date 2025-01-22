
# File: `populateuser.py`
Path: `SWARDEN.account.management.commands`



---

## Imports

### `#!py import choice`

Path: `#!py random`

Category: Native

??? example "SNIPPET"

    ```py
    from random import choice
    ```

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
            self.stdout.write('\nPopulating account.User')
            with open('./account/management/commands/populate_user.txt') as sample:
                lines: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
            for i in tqdm(lines, desc='Users', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
                (username, email, password) = i
                user: User = User.objects.create_user(username=username, email=email, password=password)
                if choice([True, False]):
                    user.is_active = False
                user.save()
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
        self.stdout.write('\nPopulating account.User')
        with open('./account/management/commands/populate_user.txt') as sample:
            lines: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]
        for i in tqdm(lines, desc='Users', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'):
            (username, email, password) = i
            user: User = User.objects.create_user(username=username, email=email, password=password)
            if choice([True, False]):
                user.is_active = False
            user.save()
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
