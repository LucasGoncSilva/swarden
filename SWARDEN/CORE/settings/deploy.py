from CORE.settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DATABASE_NAME'),
        'USER': getenv('DATABASE_USER'),
        'PASSWORD': getenv('DATABASE_PASSWORD'),
        'HOST': getenv('DATABASE_HOST'),
        'PORT': '5432',
    }
}

DEBUG = bool(getenv('DEBUG'))
SECRET_KEY = getenv('SECRET_KEY')
ALLOWED_HOSTS = list(str(getenv('ALLOWED_HOSTS')))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER: str | None = getenv('SWARDEN_EMAIL_DOMAIN')
EMAIL_HOST_PASSWORD: str | None = getenv('SWARDEN_EMAIL_PASSWORD')

# http -> https redirect
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
