from typing import Final

from django.db.models import Model, CharField, DateTimeField


# Create your models here.
class Attempt(Model):
    IP: Final[CharField] = CharField(max_length=64)
    username: Final[CharField] = CharField(max_length=64, verbose_name='Nome de Usuário')
    password: Final[CharField] = CharField(max_length=64, verbose_name='Senha')
    url: Final[CharField] = CharField(max_length=64)
    timestamp: Final[DateTimeField] = DateTimeField(auto_now_add=True, verbose_name='Data e Horário')

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __str__(self) -> str:
        date = self.timestamp
        return f'{self.pk}: {date.day}/{date.month}/{date.year} ({date.hour}h{date.minute}\'{date.second}\") UTC+3'
