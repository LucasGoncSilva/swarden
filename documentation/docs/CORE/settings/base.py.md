
# File: `base.py`
Path: `SWARDEN.CORE.settings`



---

## Imports

### `#!py import Path`

Path: `#!py pathlib`

Category: Native

??? example "SNIPPET"

    ```py
    from pathlib import Path
    ```

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import constants`

Path: `#!py django.contrib.messages`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.messages import constants
    ```



---

## Consts

### `#!py BASE_DIR`

Type: `#!py Unknown`

Value: `#!py Path(__file__).resolve().parent.parent.parent`

??? example "SNIPPET"

    ```py
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    ```

### `#!py SECRET_KEY`

Type: `#!py str`

Value: `#!py 'cw%t5oij*-s6g8xmgkp6__4br))7&01!3+6_r7vw0p6y37aztqvc_@_tz+oo!ga9&-=2_%!qx+k(0e=y)!i_e=s+5vlzonba^m3)'`

??? example "SNIPPET"

    ```py
    SECRET_KEY: str = 'cw%t5oij*-s6g8xmgkp6__4br))7&01!3+6_r7vw0p6y37aztqvc_@_tz+oo!ga9&-=2_%!qx+k(0e=y)!i_e=s+5vlzonba^m3)'
    ```

### `#!py DEBUG`

Type: `#!py bool`

Value: `#!py True`

??? example "SNIPPET"

    ```py
    DEBUG: bool = True
    ```

### `#!py ALLOWED_HOSTS`

Type: `#!py list[str]`

Value: `#!py ['*', 'localhost']`

??? example "SNIPPET"

    ```py
    ALLOWED_HOSTS: list[str] = ['*', 'localhost']
    ```

### `#!py SESSION_COOKIE_SECURE`

Type: `#!py bool`

Value: `#!py True`

??? example "SNIPPET"

    ```py
    SESSION_COOKIE_SECURE: bool = True
    ```

### `#!py CSRF_COOKIE_SECURE`

Type: `#!py bool`

Value: `#!py True`

??? example "SNIPPET"

    ```py
    CSRF_COOKIE_SECURE: bool = True
    ```

### `#!py INSTALLED_APPS`

Type: `#!py list[str]`

Value: `#!py ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'crispy_forms', 'crispy_bootstrap4', 'whitenoise', 'captcha', 'account', 'honeypot', 'home', 'secret', 'err', 'mail', 'general']`

??? example "SNIPPET"

    ```py
    INSTALLED_APPS: list[str] = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'crispy_forms', 'crispy_bootstrap4', 'whitenoise', 'captcha', 'account', 'honeypot', 'home', 'secret', 'err', 'mail', 'general']
    ```

### `#!py MIDDLEWARE`

Type: `#!py list[str]`

Value: `#!py ['django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']`

??? example "SNIPPET"

    ```py
    MIDDLEWARE: list[str] = ['django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']
    ```

### `#!py ROOT_URLCONF`

Type: `#!py Final[str]`

Value: `#!py 'CORE.urls'`

??? example "SNIPPET"

    ```py
    ROOT_URLCONF: Final[str] = 'CORE.urls'
    ```

### `#!py TEMPLATES`

Type: `#!py Final[list[dict[str, str | list[Path] | bool | dict[str, list[str]]]]]`

Value: `#!py [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]`

??? example "SNIPPET"

    ```py
    TEMPLATES: Final[list[dict[str, str | list[Path] | bool | dict[str, list[str]]]]] = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
    ```

### `#!py WSGI_APPLICATION`

Type: `#!py Final[str]`

Value: `#!py 'CORE.wsgi.application'`

??? example "SNIPPET"

    ```py
    WSGI_APPLICATION: Final[str] = 'CORE.wsgi.application'
    ```

### `#!py DATABASES`

Type: `#!py dict[str, dict[str, str | Path]]`

Value: `#!py {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}`

??? example "SNIPPET"

    ```py
    DATABASES: dict[str, dict[str, str | Path]] = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
    ```

### `#!py AUTH_PASSWORD_VALIDATORS`

Type: `#!py list[dict[str, str]]`

Value: `#!py [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]`

??? example "SNIPPET"

    ```py
    AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
    ```

### `#!py LANGUAGE_CODE`

Type: `#!py Final[str]`

Value: `#!py 'pt-br'`

??? example "SNIPPET"

    ```py
    LANGUAGE_CODE: Final[str] = 'pt-br'
    ```

### `#!py TIME_ZONE`

Type: `#!py Final[str]`

Value: `#!py 'America/Sao_Paulo'`

??? example "SNIPPET"

    ```py
    TIME_ZONE: Final[str] = 'America/Sao_Paulo'
    ```

### `#!py USE_I18N`

Type: `#!py Final[bool]`

Value: `#!py True`

??? example "SNIPPET"

    ```py
    USE_I18N: Final[bool] = True
    ```

### `#!py USE_TZ`

Type: `#!py Final[bool]`

Value: `#!py True`

??? example "SNIPPET"

    ```py
    USE_TZ: Final[bool] = True
    ```

### `#!py STATIC_URL`

Type: `#!py Final[str]`

Value: `#!py '/static/'`

??? example "SNIPPET"

    ```py
    STATIC_URL: Final[str] = '/static/'
    ```

### `#!py STATIC_ROOT`

Type: `#!py Final[Path]`

Value: `#!py BASE_DIR / 'staticfiles'`

??? example "SNIPPET"

    ```py
    STATIC_ROOT: Final[Path] = BASE_DIR / 'staticfiles'
    ```

### `#!py STATICFILES_DIRS`

Type: `#!py Final[list[Path]]`

Value: `#!py [BASE_DIR / 'static']`

??? example "SNIPPET"

    ```py
    STATICFILES_DIRS: Final[list[Path]] = [BASE_DIR / 'static']
    ```

### `#!py STATICFILES_STORAGE`

Type: `#!py Final[str]`

Value: `#!py 'whitenoise.storage.CompressedManifestStaticFilesStorage'`

??? example "SNIPPET"

    ```py
    STATICFILES_STORAGE: Final[str] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    ```

### `#!py DEFAULT_AUTO_FIELD`

Type: `#!py Final[str]`

Value: `#!py 'django.db.models.BigAutoField'`

??? example "SNIPPET"

    ```py
    DEFAULT_AUTO_FIELD: Final[str] = 'django.db.models.BigAutoField'
    ```

### `#!py AUTH_USER_MODEL`

Type: `#!py Final[str]`

Value: `#!py 'account.User'`

??? example "SNIPPET"

    ```py
    AUTH_USER_MODEL: Final[str] = 'account.User'
    ```

### `#!py LOGOUT_REDIRECT_URL`

Type: `#!py Final[str]`

Value: `#!py 'conta/entrar'`

??? example "SNIPPET"

    ```py
    LOGOUT_REDIRECT_URL: Final[str] = 'conta/entrar'
    ```

### `#!py CRISPY_ALLOWED_TEMPLATE_PACKS`

Type: `#!py Final[str]`

Value: `#!py 'bootstrap4'`

??? example "SNIPPET"

    ```py
    CRISPY_ALLOWED_TEMPLATE_PACKS: Final[str] = 'bootstrap4'
    ```

### `#!py CRISPY_TEMPLATE_PACK`

Type: `#!py Final[str]`

Value: `#!py 'bootstrap4'`

??? example "SNIPPET"

    ```py
    CRISPY_TEMPLATE_PACK: Final[str] = 'bootstrap4'
    ```

### `#!py EMAIL_BACKEND`

Type: `#!py str`

Value: `#!py 'django.core.mail.backends.console.EmailBackend'`

??? example "SNIPPET"

    ```py
    EMAIL_BACKEND: str = 'django.core.mail.backends.console.EmailBackend'
    ```

### `#!py EMAIL_HOST`

Type: `#!py str`

Value: `#!py 'smtp.gmail.com'`

??? example "SNIPPET"

    ```py
    EMAIL_HOST: str = 'smtp.gmail.com'
    ```

### `#!py EMAIL_PORT`

Type: `#!py int`

Value: `#!py 587`

??? example "SNIPPET"

    ```py
    EMAIL_PORT: int = 587
    ```

### `#!py EMAIL_USE_TLS`

Type: `#!py bool`

Value: `#!py True`

??? example "SNIPPET"

    ```py
    EMAIL_USE_TLS: bool = True
    ```

### `#!py MESSAGE_TAGS`

Type: `#!py dict[int, str]`

Value: `#!py {messages.DEBUG: 'alert-primary', messages.INFO: 'alert-info', messages.SUCCESS: 'alert-success', messages.WARNING: 'alert-warning', messages.ERROR: 'alert-danger'}`

??? example "SNIPPET"

    ```py
    MESSAGE_TAGS: dict[int, str] = {messages.DEBUG: 'alert-primary', messages.INFO: 'alert-info', messages.SUCCESS: 'alert-success', messages.WARNING: 'alert-warning', messages.ERROR: 'alert-danger'}
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
