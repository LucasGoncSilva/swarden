
# File: `views.py`
Path: `SWARDEN.general`



---

## Imports

### `#!py import login_required`

Path: `#!py django.contrib.auth.decorators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth.decorators import login_required
    ```

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import render`

Path: `#!py django.shortcuts`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.shortcuts import render
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def index`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py login_required(login_url='/conta/entrar')`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_required(login_url='/conta/entrar')
    def index(r: HttpRequest) -> HttpResponse:
        return render(r, 'general/index.html')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
