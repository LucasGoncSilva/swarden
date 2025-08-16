# File: `models.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.mail`

No file docstring provided.

---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Final
    ```

### `#!py import DateField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import DateField
    ```

### `#!py import Model`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import Model
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class WakeDatabase`

Parents: `Model`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class WakeDatabase(Model):
        created: Final[DateField] = DateField(auto_created=True, auto_now_add=True)
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
