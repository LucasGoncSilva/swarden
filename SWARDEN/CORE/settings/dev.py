# ruff: noqa: F402 F403 F405

from os import environ, getenv
from pathlib import Path
from typing import cast

from decouple import Csv, config

from CORE.settings.base import *


environ['CRYPTOSEED'] = 'just-a-not-so-long-random-string-to-emulate-a-seed'


DATABASES: dict[
    str,
    dict[
        str,
        str | bool | int | Path | dict[str, str | bool | int | dict[str, int]] | None,
    ],
] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DATABASE_NAME', 'postgres'),
        'USER': getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': getenv('DATABASE_PASSWORD', 'postgres'),
        'HOST': getenv('DATABASE_HOST', 'localhost'),
        'PORT': '5432',
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'pool': {
                'min_size': 10,
                'max_size': 32,
                'timeout': 30,
                'max_idle': 300,
            },
            'server_side_binding': True,
            'target_session_attrs': 'read-write',
            'connect_timeout': 10,
        },
    }
}

SECURE_CSP['font-src'] += ['https://fonts.gstatic.com/']
SECURE_CSP['style-src'] += ['http://fonts.googleapis.com/']

IS_LOG_ON: bool = config('IS_LOG_ON', default=IS_LOG_ON, cast=bool)

DEBUG: bool = config('DEBUG', default=DEBUG, cast=bool)
SECRET_KEY: str = cast(str, config('SECRET_KEY', default=SECRET_KEY))
ALLOWED_HOSTS: list[str] = cast(
    list[str], config('ALLOWED_HOSTS', default='*', cast=Csv())
)

CRYPTOGRAPHY_KEY: str = cast(str, config('CRYPTOGRAPHY_KEY', default=CRYPTOGRAPHY_KEY))
SYSTEM_PEPPER: str = cast(str, config('SYSTEM_PEPPER', default=SYSTEM_PEPPER))

CAPTCHA_TEST_MODE: bool = config('CAPTCHA_TEST_MODE', default=True, cast=bool)

if DEBUG:
    INSTALLED_APPS += ['django_extensions', 'debug_toolbar', 'django_dbml']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS: list[str] = ['127.0.0.1']

# Test Runner
TEST_RUNNER: Final[str] = 'CORE.testcase.GlobalSetupRunner'
