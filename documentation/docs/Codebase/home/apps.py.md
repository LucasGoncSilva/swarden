
# File: `apps.py`
Path: `SWARDEN.home`



---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import AppConfig`

Path: `#!py django.apps`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.apps import AppConfig
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class HomeConfig`

Parents: `AppConfig`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class HomeConfig(AppConfig):
        default_auto_field: Final[str] = 'django.db.models.BigAutoField'
        name: Final[str] = 'home'
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
