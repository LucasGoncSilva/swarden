from datetime import datetime
from typing import Final
from uuid import uuid4

from django.db.models import Model, CharField, DateTimeField, UUIDField
from django.core.validators import MaxLengthValidator


# Create your models here.
class Attempt(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    IP: Final[CharField] = CharField(max_length=64, validators=[MaxLengthValidator(64)])
    username: Final[CharField] = CharField(
        max_length=256,
        verbose_name='Nome de Usuário',
        validators=[MaxLengthValidator(256)],
        blank=True,
        null=True,
    )
    password: Final[CharField] = CharField(
        max_length=256,
        verbose_name='Senha',
        validators=[MaxLengthValidator(256)],
        blank=True,
        null=True,
    )
    URL: Final[CharField] = CharField(
        max_length=256, validators=[MaxLengthValidator(256)]
    )
    timestamp: Final[DateTimeField] = DateTimeField(
        auto_now_add=True, verbose_name='Data e Hora'
    )

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __str__(self) -> str:
        date = self.timestamp
        return f'{self.pk}: {date.day}/{date.month}/{date.year} ({date.hour}h{date.minute}\'{date.second}\") UTC+3'

    def is_valid(self) -> bool:
        if (
            self.IP
            and len(self.IP) <= 64
            and self.username
            and len(self.username) <= 256
            and self.password
            and len(self.password) <= 256
            and self.URL
            and len(self.URL) <= 256
            and self.timestamp
            and isinstance(self.timestamp, datetime)
        ):
            return True
        return False
