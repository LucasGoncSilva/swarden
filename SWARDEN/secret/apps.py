from typing import Final

from django.apps import AppConfig


class SecretConfig(AppConfig):
    default_auto_field: Final[str] = "django.db.models.BigAutoField"
    name: Final[str] = "secret"
    verbose_name: Final[str] = "Segredo"
