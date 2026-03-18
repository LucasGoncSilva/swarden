# ruff: noqa: F403 F405

from os import getenv
from pathlib import Path

from CORE.settings.base import *


# ===== Configs Definition =====
DATABASE_NAME_CFG: Final[str | None] = getenv('DATABASE_NAME')
DATABASE_USER_CFG: Final[str | None] = getenv('DATABASE_USER')
DATABASE_PASSWORD_CFG: Final[str | None] = getenv('DATABASE_PASSWORD')
DATABASE_HOST_CFG: Final[str | None] = getenv('DATABASE_HOST')

SECRET_KEY_CFG: Final[str | None] = getenv('SECRET_KEY')
CRYPTOGRAPHY_KEY_CFG: Final[str | None] = getenv('CRYPTOGRAPHY_KEY')
SYSTEM_PEPPER_CFG: Final[str | None] = getenv('SYSTEM_PEPPER')
ALLOWED_HOSTS_CFG: Final[str | None] = getenv('ALLOWED_HOSTS')

REDIS_HOST_CFG: Final[str | None] = getenv('REDIS_HOST')


# ===== Configs Validation =====
if getenv('ADMIN') is None:
    raise ValueError('"ADMIN" MUST be set as a valid URL path.')

if (
    DATABASE_NAME_CFG is None
    or DATABASE_USER_CFG is None
    or DATABASE_PASSWORD_CFG is None
    or DATABASE_HOST_CFG is None
):
    raise ValueError('Database configs MUST be set.')

if SECRET_KEY_CFG is None:
    raise ValueError('"SECRET_KEY" MUST be set as a valid long, pseudo-random string.')

if CRYPTOGRAPHY_KEY_CFG is None:
    raise ValueError(
        '"CRYPTOGRAPHY_KEY" MUST be set as a valid long, pseudo-random string.'
    )

if SYSTEM_PEPPER_CFG is None:
    raise ValueError(
        '"SYSTEM_PEPPER" MUST be set as a valid long, pseudo-random string.'
    )

if ALLOWED_HOSTS_CFG is None:
    raise ValueError('"ALLOWED_HOSTS" MUST be set as a valid csv-like domains list.')

if REDIS_HOST_CFG is None:
    raise ValueError('"REDIS_HOST" MUST be set as a valid host.')


# ===== Configs Usage =====
DATABASES: dict[
    str,
    dict[
        str,
        str | bool | int | Path | dict[str, str | bool | int | dict[str, int]] | None,
    ],
] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME_CFG,
        'USER': DATABASE_USER_CFG,
        'PASSWORD': DATABASE_PASSWORD_CFG,
        'HOST': DATABASE_HOST_CFG,
        'PORT': '5432',
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'pool': {
                'min_size': 2,
                'max_size': 10,
                'timeout': 30,
                'max_idle': 300,
            },
            'server_side_binding': True,
            'target_session_attrs': 'read-write',
            'connect_timeout': 10,
        },
    }
}

RATELIMIT_BACKENDS: list[dict[str, str | dict[str, str | int]]] = [
    {
        'name': 'primary_redis',
        'backend': 'redis',
        'config': {
            'host': REDIS_HOST_CFG,
            'port': 6379,
            'db': 0,
        },
    },
    {
        'name': 'fallback_memory',
        'backend': 'memory',
        'config': {},
    },
]


DEBUG: Final[bool] = False
SECRET_KEY: Final[str] = SECRET_KEY
CRYPTOGRAPHY_KEY: Final[str] = CRYPTOGRAPHY_KEY
SYSTEM_PEPPER: Final[str] = SYSTEM_PEPPER
ALLOWED_HOSTS: Final[list[str]] = ALLOWED_HOSTS

# General Security
SECURE_SSL_REDIRECT: Final[bool] = True
CSRF_COOKIE_SECURE: Final[bool] = True
SESSION_COOKIE_SECURE: Final[bool] = True
SESSION_COOKIE_SAMESITE: Final[str] = 'Strict'

# Logging
IS_LOG_ON: Final[bool] = True
