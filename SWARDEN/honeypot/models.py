from django.db.models import Model, CharField, DateTimeField


# Create your models here.
class Attempt(Model):
    IP = CharField(max_length=64)
    username = CharField(max_length=64, verbose_name='Nome de Usuário')
    password = CharField(max_length=64, verbose_name='Senha')
    url = CharField(max_length=64)
    timestamp = DateTimeField(auto_now_add=True, verbose_name='Data e Horário')

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __str__(self) -> str:
        date = self.timestamp
        return f'{self.pk}: {date.day}/{date.month}/{date.year} ({date.hour}h{date.minute}\'{date.second}\") UTC+3'
