from os import getenv
from pathlib import Path
from typing import Final, Literal

from django.contrib.messages import constants as messages
from django.utils.csp import CSP
from mnemonic import Mnemonic


# Defines for the entire project if in dev environment or not
IS_DEV_ENVIRONMENT: Final[bool] = (
    getenv('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev') == 'CORE.settings.dev'
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = 'cw%t5oij*-s6g8xmgkp6__4br))7&01!3+6_r7vw0p6y37aztqvc_@_tz+oo!ga9&-=2_%!qx+k(0e=y)!i_e=s+5vlzonba^m3)'  # noqa: E501
CRYPTOGRAPHY_KEY: str = '88pfvg(r6t=&_cka5uo*zvs8p!!&rh62p_klf_)!qe9ib^ny!@!q++$377c0wuh71rjn$6h93^-yqv&#b^%8@5aq!9&zfvj*d4zy'  # noqa: E501
SYSTEM_PEPPER: str = 'cbg8y%_$%mg47gu*1usc4hsg=%s2keqt5#!6&0y3@e7=z$c3q%b5i55!1_3*o%vscj$%sl0%+#gmwv)i(3)utp28hs$q9a#)ehgg'  # noqa: E501


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = True
ALLOWED_HOSTS: list[str] = ['*', 'localhost']

CSRF_COOKIE_NAME: Final[str] = 'crosstoken'
CSRF_COOKIE_HTTPONLY: Final[bool] = True

SECURE_CROSS_ORIGIN_OPENER_POLICY: Final[str] = 'same-origin'
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY: Final[str] = 'require-corp'
SECURE_CROSS_ORIGIN_RESOURCE_POLICY: Final[str] = 'same-origin'

SESSION_COOKIE_HTTPONLY: Final[bool] = True
SESSION_COOKIE_NAME: Final[str] = 'sid'

SECURE_PROXY_SSL_HEADER: Final[tuple[str, str]] = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS: Final[int] = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS: Final[bool] = True
SECURE_HSTS_PRELOAD: Final[bool] = True

SECURE_BROWSER_XSS_FILTER: Final[bool] = True

SECURE_CONTENT_TYPE_NOSNIFF: Final[bool] = True

SECURE_REFERRER_POLICY: Final[str] = 'strict-origin'

X_FRAME_OPTIONS: Final[str] = 'DENY'


# Application definition
INSTALLED_APPS: list[str] = [
    # Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party
    'whitenoise',
    'captcha',
    'django_smart_ratelimit',
    # Local
    'account',
    'home',
    'secret',
    'err',
    'plans',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'CORE.middlewares.logger.WideEventLoggingMiddleware',
    'django.middleware.csp.ContentSecurityPolicyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'CORE.middlewares.ratelimit.RateLimitMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: Final[str] = 'CORE.urls'

TEMPLATES: Final[list[dict[str, str | list[Path] | bool | dict[str, list[str]]]]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.csp',
            ],
        },
    },
]

WSGI_APPLICATION: Final[str] = 'CORE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES: dict[str, dict[str, str | Path]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE: Final[str] = 'en'

TIME_ZONE: Final[str] = 'America/Sao_Paulo'

USE_I18N: Final[bool] = True

USE_TZ: Final[bool] = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL: Final[str] = '/assets/'
STATIC_ROOT: Final[Path] = BASE_DIR / 'staticfiles'
STATICFILES_DIRS: Final[list[Path]] = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE: Final[str] = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

default_auto_field: str = 'django.db.models.BigAutoField'


# User Model
AUTH_USER_MODEL: Final[str] = 'account.User'
LOGOUT_REDIRECT_URL: Final[str] = 'account/login'


# Argon2 Hash Algo
PASSWORD_HASHERS: list[str] = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]


# Messages configs
MESSAGE_TAGS: dict[int, str] = {
    messages.DEBUG: 'alert-debug',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-error',
}


# CSP - Content Security Policy
SECURE_CSP: dict[str, list[CSP | str]] = {
    'default-src': [CSP.SELF],
    'script-src': [CSP.SELF, CSP.NONCE],
    'img-src': [CSP.SELF, CSP.NONCE],
    'font-src': [CSP.SELF, CSP.NONCE],
    'style-src': [CSP.SELF, CSP.NONCE],
}


# Default Login URL
LOGIN_URL: Final[str] = '/account/login'


# Mnemonic Object
MNEMONIC: Final[Mnemonic] = Mnemonic()


# Captcha
CAPTCHA_ANIMATED: Final[bool] = True
CAPTCHA_BACKGROUND_COLOR: Final[str] = '#0e121a'
CAPTCHA_FOREGROUND_COLOR: Final[str] = '#34d399'


# Rate Limiting
RATELIMIT_ENABLE: bool = False if IS_DEV_ENVIRONMENT else True
RATELIMIT_BACKENDS: list[dict[str, str | dict[str, str | int]]] = [
    {
        'name': 'primary_redis',
        'backend': 'redis',
        'config': {
            'host': 'localhost',
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
RATELIMIT_ALGORITHM: Final[
    Literal['sliding_window', 'fixed_window', 'token_bucket', 'leaky_bucket']
] = 'sliding_window'
RATELIMIT_MULTI_BACKEND_STRATEGY: Final[str] = 'first_healthy'
RATELIMIT_DEFAULT_LIMIT: Final[str] = '60/m'
RATELIMIT_ALIGN_WINDOW_TO_CLOCK: Final[bool] = False


# Logging
IS_LOG_ON: bool = False
LOGGING: dict[str, int | bool | dict[str, dict[str, list[str] | str | bool]]] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'format': '%(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'loggers': {
        'wide_events': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
