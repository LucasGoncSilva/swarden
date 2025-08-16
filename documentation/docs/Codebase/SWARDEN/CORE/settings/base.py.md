# File: `base.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.CORE.settings`

No file docstring provided.

---

## Imports

### `#!py import Path`

Path: `#!py pathlib`

Category: native

??? example "Snippet"

    ```py
    from pathlib import Path
    ```

### `#!py import Final`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Final
    ```

### `#!py import constants`

Path: `#!py django.contrib.messages`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.messages import constants
    ```



---

## Consts

### `#!py BASE_DIR`

Type: `#!py Unknown`

Value: `#!py Path(__file__).resolve().parent.parent.parent`

??? example "Snippet"

    ```py
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    ```

### `#!py SECRET_KEY`

Type: `#!py str`

Value: `#!py 'cw%t5oij*-s6g8xmgkp6__4br))7&01!3+6_r7vw0p6y37aztqvc_@_tz+oo!ga9&-=2_%!qx+k(0e=y)!i_e=s+5vlzonba^m3)'`

??? example "Snippet"

    ```py
    SECRET_KEY: str = 'cw%t5oij*-s6g8xmgkp6__4br))7&01!3+6_r7vw0p6y37aztqvc_@_tz+oo!ga9&-=2_%!qx+k(0e=y)!i_e=s+5vlzonba^m3)'
    ```

### `#!py DEBUG`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    DEBUG: bool = True
    ```

### `#!py ALLOWED_HOSTS`

Type: `#!py list[str]`

Value: `#!py ['*', 'localhost']`

??? example "Snippet"

    ```py
    ALLOWED_HOSTS: list[str] = ['*', 'localhost']
    ```

### `#!py SESSION_COOKIE_SECURE`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    SESSION_COOKIE_SECURE: bool = True
    ```

### `#!py CSRF_COOKIE_SECURE`

Type: `#!py bool`

Value: `#!py True`

??? example "Snippet"

    ```py
    CSRF_COOKIE_SECURE: bool = True
    ```

### `#!py INSTALLED_APPS`

Type: `#!py list[str]`

Value: `#!py ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'whitenoise', 'captcha', 'csp', 'account', 'home', 'secret', 'err', 'mail', 'general', 'plans']`

??? example "Snippet"

    ```py
    INSTALLED_APPS: list[str] = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'whitenoise', 'captcha', 'csp', 'account', 'home', 'secret', 'err', 'mail', 'general', 'plans']
    ```

### `#!py MIDDLEWARE`

Type: `#!py list[str]`

Value: `#!py ['django.middleware.security.SecurityMiddleware', 'csp.middleware.CSPMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']`

??? example "Snippet"

    ```py
    MIDDLEWARE: list[str] = ['django.middleware.security.SecurityMiddleware', 'csp.middleware.CSPMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']
    ```

### `#!py ROOT_URLCONF`

Type: `#!py Final[str]`

Value: `#!py 'CORE.urls'`

??? example "Snippet"

    ```py
    ROOT_URLCONF: Final[str] = 'CORE.urls'
    ```

### `#!py TEMPLATES`

Type: `#!py Final[list[dict[str, str | list[Path] | bool | dict[str, list[str]]]]]`

Value: `#!py [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]`

??? example "Snippet"

    ```py
    TEMPLATES: Final[list[dict[str, str | list[Path] | bool | dict[str, list[str]]]]] = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
    ```

### `#!py WSGI_APPLICATION`

Type: `#!py Final[str]`

Value: `#!py 'CORE.wsgi.application'`

??? example "Snippet"

    ```py
    WSGI_APPLICATION: Final[str] = 'CORE.wsgi.application'
    ```

### `#!py DATABASES`

Type: `#!py dict[str, dict[str, str | Path]]`

Value: `#!py {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}`

??? example "Snippet"

    ```py
    DATABASES: dict[str, dict[str, str | Path]] = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
    ```

### `#!py AUTH_PASSWORD_VALIDATORS`

Type: `#!py list[dict[str, str]]`

Value: `#!py [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]`

??? example "Snippet"

    ```py
    AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
    ```

### `#!py LANGUAGE_CODE`

Type: `#!py Final[str]`

Value: `#!py 'en'`

??? example "Snippet"

    ```py
    LANGUAGE_CODE: Final[str] = 'en'
    ```

### `#!py TIME_ZONE`

Type: `#!py Final[str]`

Value: `#!py 'America/Sao_Paulo'`

??? example "Snippet"

    ```py
    TIME_ZONE: Final[str] = 'America/Sao_Paulo'
    ```

### `#!py USE_I18N`

Type: `#!py Final[bool]`

Value: `#!py True`

??? example "Snippet"

    ```py
    USE_I18N: Final[bool] = True
    ```

### `#!py USE_TZ`

Type: `#!py Final[bool]`

Value: `#!py True`

??? example "Snippet"

    ```py
    USE_TZ: Final[bool] = True
    ```

### `#!py STATIC_URL`

Type: `#!py Final[str]`

Value: `#!py '/static/'`

??? example "Snippet"

    ```py
    STATIC_URL: Final[str] = '/static/'
    ```

### `#!py STATIC_ROOT`

Type: `#!py Final[Path]`

Value: `#!py BASE_DIR / 'staticfiles'`

??? example "Snippet"

    ```py
    STATIC_ROOT: Final[Path] = BASE_DIR / 'staticfiles'
    ```

### `#!py STATICFILES_DIRS`

Type: `#!py Final[list[Path]]`

Value: `#!py [BASE_DIR / 'static']`

??? example "Snippet"

    ```py
    STATICFILES_DIRS: Final[list[Path]] = [BASE_DIR / 'static']
    ```

### `#!py STATICFILES_STORAGE`

Type: `#!py Final[str]`

Value: `#!py 'whitenoise.storage.CompressedManifestStaticFilesStorage'`

??? example "Snippet"

    ```py
    STATICFILES_STORAGE: Final[str] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    ```

### `#!py DEFAULT_AUTO_FIELD`

Type: `#!py Final[str]`

Value: `#!py 'django.db.models.BigAutoField'`

??? example "Snippet"

    ```py
    DEFAULT_AUTO_FIELD: Final[str] = 'django.db.models.BigAutoField'
    ```

### `#!py AUTH_USER_MODEL`

Type: `#!py Final[str]`

Value: `#!py 'account.User'`

??? example "Snippet"

    ```py
    AUTH_USER_MODEL: Final[str] = 'account.User'
    ```

### `#!py LOGOUT_REDIRECT_URL`

Type: `#!py Final[str]`

Value: `#!py 'account/login'`

??? example "Snippet"

    ```py
    LOGOUT_REDIRECT_URL: Final[str] = 'account/login'
    ```

### `#!py PASSWORD_HASHERS`

Type: `#!py list[str]`

Value: `#!py ['django.contrib.auth.hashers.Argon2PasswordHasher', 'django.contrib.auth.hashers.PBKDF2PasswordHasher', 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher', 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher', 'django.contrib.auth.hashers.ScryptPasswordHasher']`

??? example "Snippet"

    ```py
    PASSWORD_HASHERS: list[str] = ['django.contrib.auth.hashers.Argon2PasswordHasher', 'django.contrib.auth.hashers.PBKDF2PasswordHasher', 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher', 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher', 'django.contrib.auth.hashers.ScryptPasswordHasher']
    ```

### `#!py MESSAGE_TAGS`

Type: `#!py dict[int, str]`

Value: `#!py {messages.DEBUG: 'alert-debug', messages.INFO: 'alert-info', messages.SUCCESS: 'alert-success', messages.WARNING: 'alert-warning', messages.ERROR: 'alert-error'}`

??? example "Snippet"

    ```py
    MESSAGE_TAGS: dict[int, str] = {messages.DEBUG: 'alert-debug', messages.INFO: 'alert-info', messages.SUCCESS: 'alert-success', messages.WARNING: 'alert-warning', messages.ERROR: 'alert-error'}
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
