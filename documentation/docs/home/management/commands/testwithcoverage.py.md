
# File: `testwithcoverage.py`
Path: `SWARDEN.home.management.commands`



---

## Imports

### `#!py import system`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import system
    ```

### `#!py import Any`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Any
    ```

### `#!py import Literal`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Literal
    ```

### `#!py import BaseCommand`

Path: `#!py django.core.management`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.management import BaseCommand
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

        def add_arguments(self, parser):
            parser.add_argument('--app', type=str, help='App to be covered - "." if nothing is defined.', default='.')

        def handle(self, *args: Any, **options: Any) -> None:
            omit_list: list[str] = ['*/month/*,', '*/migrations/*,', '*/admin.py,', 'manage.py,', '*/CORE/*,']
            app: Literal['.'] | str = options['app']
            source: str = f"--source='{app}'"
            omit: str = f"--omit='{','.join(omit_list)}'"
            cmd: str = f'coverage run {source} {omit} manage.py test {app}'
            system(cmd)
            system('coverage html')
            self.stdout.write(self.style.SUCCESS('Coverage done + HTML file generated.'))
    ```



---

## Functions

### `#!py def add_arguments`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, parser: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def add_arguments(self, parser):
        parser.add_argument('--app', type=str, help='App to be covered - "." if nothing is defined.', default='.')
    ```

### `#!py def handle`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def handle(self, *args: Any, **options: Any) -> None:
        omit_list: list[str] = ['*/month/*,', '*/migrations/*,', '*/admin.py,', 'manage.py,', '*/CORE/*,']
        app: Literal['.'] | str = options['app']
        source: str = f"--source='{app}'"
        omit: str = f"--omit='{','.join(omit_list)}'"
        cmd: str = f'coverage run {source} {omit} manage.py test {app}'
        system(cmd)
        system('coverage html')
        self.stdout.write(self.style.SUCCESS('Coverage done + HTML file generated.'))
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
