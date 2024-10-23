# ruff: noqa: F403

from os import getenv

import dj_database_url
from CORE.settings.base import *


DATABASES = {'default': dj_database_url.config(default=str(getenv('DATABASE_URL')))}

DEBUG: bool = bool(getenv('DEBUG', False))
SECRET_KEY: str | None = getenv('SECRET_KEY')
ALLOWED_HOSTS: list[str] = list(
    map(lambda url: url.strip(), str(getenv('ALLOWED_HOSTS')).split(','))
)

EMAIL_BACKEND: str = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER: str | None = getenv('SWARDEN_EMAIL_DOMAIN')
EMAIL_HOST_PASSWORD: str | None = getenv('SWARDEN_EMAIL_PASSWORD')

# http -> https redirect
SECURE_PROXY_SSL_HEADER: tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT: bool = True
