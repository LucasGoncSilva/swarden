# File: `deploy.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.CORE.settings`

No file docstring provided.

---

## Imports

### `#!py import getenv`

Path: `#!py os`

Category: native

??? example "Snippet"

    ```py
    from os import getenv
    ```

### `#!py import dj_database_url`

Path: `#!py None`

Category: trdparty

??? example "Snippet"

    ```py
    import dj_database_url
    ```

### `#!py import *`

Path: `#!py CORE.settings.base`

Category: trdparty

??? example "Snippet"

    ```py
    from CORE.settings.base import *
    ```

### `#!py import NONE`

Path: `#!py csp.constants`

Category: trdparty

??? example "Snippet"

    ```py
    from csp.constants import NONE
    ```

### `#!py import SELF`

Path: `#!py csp.constants`

Category: trdparty

??? example "Snippet"

    ```py
    from csp.constants import SELF
    ```



---

## Consts

### `#!py DATABASES`

Type: `#!py Unknown`

Value: `#!py {'default': dj_database_url.config(default=str(getenv('DATABASE_URL')))}`

??? example "Snippet"

    ```py
    DATABASES = {'default': dj_database_url.config(default=str(getenv('DATABASE_URL')))}
    ```

### `#!py DEBUG`

Type: `#!py bool`

Value: `#!py bool(getenv('DEBUG', False))`

??? example "Snippet"

    ```py
    DEBUG: bool = bool(getenv('DEBUG', False))
    ```

### `#!py SECRET_KEY`

Type: `#!py str | None`

Value: `#!py getenv('SECRET_KEY')`

??? example "Snippet"

    ```py
    SECRET_KEY: str | None = getenv('SECRET_KEY')
    ```

### `#!py ALLOWED_HOSTS`

Type: `#!py list[str]`

Value: `#!py list(map(lambda url: url.strip(), str(getenv('ALLOWED_HOSTS')).split(',')))`

??? example "Snippet"

    ```py
    ALLOWED_HOSTS: list[str] = list(map(lambda url: url.strip(), str(getenv('ALLOWED_HOSTS')).split(',')))
    ```

### `#!py SECURE_CROSS_ORIGIN_OPENER_POLICY`

Type: `#!py str`

Value: `#!py 'same-origin'`

??? example "Snippet"

    ```py
    SECURE_CROSS_ORIGIN_OPENER_POLICY: str = 'same-origin'
    ```

### `#!py SECURE_CROSS_ORIGIN_EMBEDDER_POLICY`

Type: `#!py str`

Value: `#!py 'require-corp'`

??? example "Snippet"

    ```py
    SECURE_CROSS_ORIGIN_EMBEDDER_POLICY: str = 'require-corp'
    ```

### `#!py SECURE_CROSS_ORIGIN_RESOURCE_POLICY`

Type: `#!py str`

Value: `#!py 'same-origin'`

??? example "Snippet"

    ```py
    SECURE_CROSS_ORIGIN_RESOURCE_POLICY: str = 'same-origin'
    ```

### `#!py SESSION_COOKIE_HTTPONLY`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    SESSION_COOKIE_HTTPONLY: bool = True
    ```

### `#!py CSRF_COOKIE_HTTPONLY`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    CSRF_COOKIE_HTTPONLY: bool = True
    ```

### `#!py SECURE_PROXY_SSL_HEADER`

Type: `#!py tuple[str, str]`

Value: `#!py ('HTTP_X_FORWARDED_PROTO', 'https')`

??? example "Snippet"

    ```py
    SECURE_PROXY_SSL_HEADER: tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
    ```

### `#!py SECURE_SSL_REDIRECT`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    SECURE_SSL_REDIRECT: bool = True
    ```

### `#!py SECURE_HSTS_SECONDS`

Type: `#!py int`

Value: `#!py 31536000`

??? example "Snippet"

    ```py
    SECURE_HSTS_SECONDS: int = 31536000
    ```

### `#!py SECURE_HSTS_INCLUDE_SUBDOMAINS`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
    ```

### `#!py SECURE_HSTS_PRELOAD`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    SECURE_HSTS_PRELOAD: bool = True
    ```

### `#!py CSRF_COOKIE_SECURE`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    CSRF_COOKIE_SECURE: bool = True
    ```

### `#!py SESSION_COOKIE_SECURE`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    SESSION_COOKIE_SECURE: bool = True
    ```

### `#!py SECURE_BROWSER_XSS_FILTER`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    SECURE_BROWSER_XSS_FILTER: bool = True
    ```

### `#!py SECURE_CONTENT_TYPE_NOSNIFF`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    SECURE_CONTENT_TYPE_NOSNIFF: bool = True
    ```

### `#!py X_FRAME_OPTIONS`

Type: `#!py str`

Value: `#!py 'DENY'`

??? example "Snippet"

    ```py
    X_FRAME_OPTIONS: str = 'DENY'
    ```

### `#!py SECURE_REFERRER_POLICY`

Type: `#!py str`

Value: `#!py 'strict-origin'`

??? example "Snippet"

    ```py
    SECURE_REFERRER_POLICY: str = 'strict-origin'
    ```

### `#!py CONTENT_SECURITY_POLICY`

Type: `#!py Unknown`

Value: `#!py {'DIRECTIVES': {'default-src': [NONE], 'script-src': [SELF], 'style-src': [SELF], 'img-src': [SELF], 'font-src': [SELF], 'connect-src': [SELF], 'frame-ancestor': [NONE], 'base-uri': [NONE], 'form-action': [SELF], 'upgrade-insecure-requests': True}}`

??? example "Snippet"

    ```py
    CONTENT_SECURITY_POLICY = {'DIRECTIVES': {'default-src': [NONE], 'script-src': [SELF], 'style-src': [SELF], 'img-src': [SELF], 'font-src': [SELF], 'connect-src': [SELF], 'frame-ancestor': [NONE], 'base-uri': [NONE], 'form-action': [SELF], 'upgrade-insecure-requests': True}}
    ```



---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
