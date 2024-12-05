
# File: `views.py`
Path: `SWARDEN.honeypot`



---

## Imports

### `#!py import Any`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Any
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

### `#!py import get_ip_address`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import get_ip_address
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

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def honeypot`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py None`

Args: `#!py r: HttpRequest, path: str | None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def honeypot(r: HttpRequest, path: str | None=None) -> HttpResponse:
        if r.method != 'POST':
            if r.user.is_authenticated:
                return render(r, 'honeypot/authenticated.html', {'next': r.path, 'user': r.user.username})
            return render(r, 'honeypot/honeypot.html', {'next': r.path})
        ip: Any | None = get_ip_address(r)
        username: str | None = r.POST.get('username')
        password: str | None = r.POST.get('password')
        url: str = r.get_full_path()
        Attempt.objects.create(IP=ip, username=username, password=password, URL=url)
        if r.user.is_authenticated:
            return render(r, 'honeypot/authenticated.html', {'next': r.path, 'user': r.user.username})
        return render(r, 'honeypot/loop.html', {'next': url})
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
