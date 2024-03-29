from typing import Final

from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, EmailField, BooleanField, DateTimeField


# Create your models here.
class User(AbstractUser):
    first_name: Final[CharField] = CharField(max_length=150, blank=True)
    last_name: Final[CharField] = CharField(max_length=150, blank=True)
    email: Final[EmailField] = EmailField(unique=True)


class ActivationAccountToken(Model):
    value: Final[CharField] = CharField(max_length=128)
    used: Final[BooleanField] = BooleanField(default=False, verbose_name='Usado?')
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token de Ativação'
        verbose_name_plural = 'Tokens de Ativação'

    def __str__(self) -> str:
        return f'{self.value}'
