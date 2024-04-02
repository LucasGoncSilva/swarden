from datetime import datetime
from email.policy import default
from typing import Final
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db.models import (
    Model,
    CharField,
    EmailField,
    BooleanField,
    DateTimeField,
    UUIDField,
)


# Create your models here.
class User(AbstractUser):
    first_name: Final[CharField] = CharField(max_length=150, blank=True)
    last_name: Final[CharField] = CharField(max_length=150, blank=True)
    email: Final[EmailField] = EmailField(unique=True)


class ActivationAccountToken(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    value: Final[CharField] = CharField(
        max_length=64, validators=[MinLengthValidator(64), MaxLengthValidator(64)]
    )
    used: BooleanField = BooleanField(default=False, verbose_name='Usado?')
    failed: BooleanField = BooleanField(default=False, verbose_name='Falhou?')
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token de Ativação'
        verbose_name_plural = 'Tokens de Ativação'

    def __str__(self) -> str:
        return f'{self.value}'

    def is_valid(self) -> bool:
        if (
            self.value
            and len(self.value) == 64
            and isinstance(self.used, bool)
            and self.created
            and isinstance(self.created, datetime)
        ):
            return True
        return False
