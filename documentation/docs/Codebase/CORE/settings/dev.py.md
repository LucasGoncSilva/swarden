
# File: `dev.py`
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

Type: `#!py dict[str, dict[str, str | Path]]`

Value: `#!py {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': getenv('DATABASE_NAME', 'postgres'), 'USER': getenv('DATABASE_USER', 'postgres'), 'PASSWORD': getenv('DATABASE_PASSWORD', 'postgres'), 'HOST': getenv('DATABASE_HOST', 'localhost'), 'PORT': '5432'}}`

??? example "SNIPPET"

    ```py
    DATABASES: dict[str, dict[str, str | Path]] = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': getenv('DATABASE_NAME', 'postgres'), 'USER': getenv('DATABASE_USER', 'postgres'), 'PASSWORD': getenv('DATABASE_PASSWORD', 'postgres'), 'HOST': getenv('DATABASE_HOST', 'localhost'), 'PORT': '5432'}}
    ```

### `#!py DEBUG`

Type: `#!py Unknown`

Value: `#!py bool(getenv('DEBUG', DEBUG))`

??? example "SNIPPET"

    ```py
    DEBUG = bool(getenv('DEBUG', DEBUG))
    ```

### `#!py SECRET_KEY`

Type: `#!py str`

Value: `#!py getenv('SECRET_KEY', SECRET_KEY)`

??? example "SNIPPET"

    ```py
    SECRET_KEY: str = getenv('SECRET_KEY', SECRET_KEY)
    ```

### `#!py ALLOWED_HOSTS`

Type: `#!py list[str]`

Value: `#!py list(str(getenv('ALLOWED_HOSTS', ALLOWED_HOSTS)))`

??? example "SNIPPET"

    ```py
    ALLOWED_HOSTS: list[str] = list(str(getenv('ALLOWED_HOSTS', ALLOWED_HOSTS)))
    ```

### `#!py CAPTCHA_TEST_MODE`

Type: `#!py bool`

Value: `#!py bool(getenv('CAPTCHA_TEST_MODE', True))`

??? example "SNIPPET"

    ```py
    CAPTCHA_TEST_MODE: bool = bool(getenv('CAPTCHA_TEST_MODE', True))
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
