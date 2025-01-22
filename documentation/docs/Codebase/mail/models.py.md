
# File: `models.py`
Path: `SWARDEN.mail`



---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import DateField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import DateField
    ```

### `#!py import Model`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

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

??? example "SNIPPET"

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
