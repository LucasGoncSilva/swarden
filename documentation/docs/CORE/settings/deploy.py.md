
# File: `deploy.py`
Path: `SWARDEN.CORE.settings`



---

## Imports

### `#!py import getenv`

Path: `#!py os`

Category: Native

??? example "SNIPPET"

    ```py
    from os import getenv
    ```

### `#!py import dj_database_url`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import dj_database_url
    ```

### `#!py import *`

Path: `#!py CORE.settings.base`

Category: Local

??? example "SNIPPET"

    ```py
    from CORE.settings.base import *
    ```



---

## Consts

### `#!py DATABASES`

Type: `#!py Unknown`

Value: `#!py {'default': dj_database_url.config(default=str(getenv('DATABASE_URL')))}`

??? example "SNIPPET"

    ```py
    DATABASES = {'default': dj_database_url.config(default=str(getenv('DATABASE_URL')))}
    ```

### `#!py DEBUG`

Type: `#!py bool`

Value: `#!py bool(getenv('DEBUG', False))`

??? example "SNIPPET"

    ```py
    DEBUG: bool = bool(getenv('DEBUG', False))
    ```

### `#!py SECRET_KEY`

Type: `#!py str | None`

Value: `#!py getenv('SECRET_KEY')`

??? example "SNIPPET"

    ```py
    SECRET_KEY: str | None = getenv('SECRET_KEY')
    ```

### `#!py ALLOWED_HOSTS`

Type: `#!py list[str]`

Value: `#!py list(map(lambda url: url.strip(), str(getenv('ALLOWED_HOSTS')).split(',')))`

??? example "SNIPPET"

    ```py
    ALLOWED_HOSTS: list[str] = list(map(lambda url: url.strip(), str(getenv('ALLOWED_HOSTS')).split(',')))
    ```

### `#!py EMAIL_BACKEND`

Type: `#!py str`

Value: `#!py 'django.core.mail.backends.smtp.EmailBackend'`

??? example "SNIPPET"

    ```py
    EMAIL_BACKEND: str = 'django.core.mail.backends.smtp.EmailBackend'
    ```

### `#!py EMAIL_HOST_USER`

Type: `#!py str | None`

Value: `#!py getenv('SWARDEN_EMAIL_DOMAIN')`

??? example "SNIPPET"

    ```py
    EMAIL_HOST_USER: str | None = getenv('SWARDEN_EMAIL_DOMAIN')
    ```

### `#!py EMAIL_HOST_PASSWORD`

Type: `#!py str | None`

Value: `#!py getenv('SWARDEN_EMAIL_PASSWORD')`

??? example "SNIPPET"

    ```py
    EMAIL_HOST_PASSWORD: str | None = getenv('SWARDEN_EMAIL_PASSWORD')
    ```

### `#!py SECURE_PROXY_SSL_HEADER`

Type: `#!py tuple[str, str]`

Value: `#!py ('HTTP_X_FORWARDED_PROTO', 'https')`

??? example "SNIPPET"

    ```py
    SECURE_PROXY_SSL_HEADER: tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
    ```

### `#!py SECURE_SSL_REDIRECT`

Type: `#!py bool`

Value: `#!py True`

??? example "SNIPPET"

    ```py
    SECURE_SSL_REDIRECT: bool = True
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
