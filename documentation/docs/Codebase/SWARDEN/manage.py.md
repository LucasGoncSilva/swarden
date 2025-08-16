# File: `manage.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN`

No file docstring provided.

---

## Imports

### `#!py import os`

Path: `#!py None`

Category: native

??? example "Snippet"

    ```py
    import os
    ```

### `#!py import sys`

Path: `#!py None`

Category: native

??? example "Snippet"

    ```py
    import sys
    ```

### `#!py import execute_from_command_line`

Path: `#!py django.core.management`

Category: trdparty

??? example "Snippet"

    ```py
    from django.core.management import execute_from_command_line
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def main`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py None`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    Run administrative tasks.

??? example "Snippet"

    ```py
    def main():
        """Run administrative tasks."""
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev')
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?") from exc
        execute_from_command_line(sys.argv)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
