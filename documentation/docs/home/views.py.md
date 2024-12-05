
# File: `views.py`
Path: `SWARDEN.home`



---

## Imports

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

### `#!py import Card`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import Card
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import SecurityNote
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

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def index(r: HttpRequest) -> HttpResponse:
        if r.user.is_authenticated:
            credentials: LoginCredential = r.user.credentials.all()
            cards: Card = r.user.cards.all()
            notes: SecurityNote = r.user.notes.all()
            return render(r, 'home/index.html', {'credentials': credentials[:4], 'cards': cards[:4], 'notes': notes[:4], 'credentials_count': credentials.count(), 'cards_count': cards.count(), 'notes_count': notes.count()})
        return render(r, 'home/landing.html')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
