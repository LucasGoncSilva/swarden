# File: `views.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.general`

No file docstring provided.

---

## Imports

### `#!py import login_required`

Path: `#!py django.contrib.auth.decorators`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.decorators import login_required
    ```

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import render`

Path: `#!py django.shortcuts`

Category: trdparty

??? example "Snippet"

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

Type: `#!py function`

Decorators: `#!py login_required(login_url='/account/login')`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_required(login_url='/account/login')
    def index(r: HttpRequest) -> HttpResponse:
        return render(r, 'general/index.html')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
