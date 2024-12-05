
# File: `views.py`
Path: `SWARDEN.err`



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



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def handle403`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def handle403(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(r, 'err/error_template.html', {'code': 403, 'message1': 'Você não tem autorização para proseguir.', 'message2': 'Retorne para onde estava ou vá para a homepage.'})
    ```

### `#!py def handle404`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def handle404(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(r, 'err/error_template.html', {'code': 404, 'message1': 'O endereço requisitado não foi encontrado.', 'message2': 'Retorne para onde estava ou vá para a homepage.'})
    ```

### `#!py def handle500`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def handle500(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(r, 'err/error_template.html', {'code': 500, 'message1': 'Ocorreu um problema com o servidor.', 'message2': 'Informe o problema para a equipe do site.'})
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
