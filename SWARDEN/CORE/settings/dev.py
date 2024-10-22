# ruff: noqa: F402 F403 F405

from os import getenv

from CORE.settings.base import *


# docker run --name psql_swarden -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres  # noqa: E501
DATABASES: dict[str, dict[str, str | Path]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DATABASE_NAME', 'postgres'),
        'USER': getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': getenv('DATABASE_PASSWORD', 'postgres'),
        'HOST': getenv('DATABASE_HOST', 'localhost'),
        'PORT': '5432',
    }
}

INSTALLED_APPS += ['django_extensions']

DEBUG = bool(getenv('DEBUG', DEBUG))
SECRET_KEY: str = getenv('SECRET_KEY', SECRET_KEY)
ALLOWED_HOSTS: list[str] = list(str(getenv('ALLOWED_HOSTS', ALLOWED_HOSTS)))
CAPTCHA_TEST_MODE: bool = bool(getenv('CAPTCHA_TEST_MODE', True))
