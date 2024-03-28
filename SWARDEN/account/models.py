from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, EmailField, BooleanField, DateTimeField


# Create your models here.
class User(AbstractUser):
    first_name: CharField = CharField(max_length=150, blank=True)
    last_name: CharField = CharField(max_length=150, blank=True)
    email: EmailField = EmailField(unique=True)


class ActivationAccountToken(Model):
    value: CharField = CharField(max_length=128)
    used: BooleanField = BooleanField(default=False, verbose_name='Usado?')
    created: DateTimeField = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token de Ativação'
        verbose_name_plural = 'Tokens de Ativação'

    def __str__(self) -> str:
        return f'{self.value}'
