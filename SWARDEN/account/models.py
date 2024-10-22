from datetime import datetime
from typing import Final
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Model,
    UUIDField,
)


class User(AbstractUser):
    first_name: Final[CharField] = CharField(
        max_length=150, blank=True, verbose_name='Nome'
    )
    last_name: Final[CharField] = CharField(
        max_length=150, blank=True, verbose_name='Sobrenome'
    )
    email: Final[EmailField] = EmailField(unique=True)


class ActivationAccountToken(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    user: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE)
    value: Final[CharField] = CharField(
        max_length=64, validators=[MinLengthValidator(64), MaxLengthValidator(64)]
    )
    used: BooleanField = BooleanField(default=False, verbose_name='Usado?')
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name: Final[str] = 'Token de Ativação'
        verbose_name_plural: Final[str] = 'Tokens de Ativação'

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
