
# File: `admin.py`
Path: `SWARDEN.honeypot`



---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import swarden_admin`

Path: `#!py CORE.admin`

Category: Local

??? example "SNIPPET"

    ```py
    from CORE.admin import swarden_admin
    ```

### `#!py import admin`

Path: `#!py django.contrib`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib import admin
    ```

### `#!py import Attempt`

Path: `#!py honeypot.models`

Category: Local

??? example "SNIPPET"

    ```py
    from honeypot.models import Attempt
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class AttempAdmin`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class AttempAdmin(admin.ModelAdmin):
        readonly_fields: Final = ('IP', 'username', 'password', 'URL', 'timestamp')
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
