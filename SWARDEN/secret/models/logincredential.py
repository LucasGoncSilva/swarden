from typing import Any, Final
from uuid import uuid4

from account.models import User
from crypt.fields import EncryptedCharField, EncryptedTextField
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db.models import (
    CASCADE,
    SET,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    SlugField,
    UUIDField,
)
from django.urls import reverse
from django.utils.text import slugify


def set_service_other() -> UUIDField:
    return Service.objects.get_or_create(name='Other')[0].pk


class Service(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    name: Final[CharField] = CharField(
        max_length=128, validators=(MaxLengthValidator(128),)
    )
    note: EncryptedTextField = EncryptedTextField(
        max_length=128,
        blank=True,
        null=True,
        validators=(MaxLengthValidator(128),),
    )
    created: Final[DateTimeField] = DateTimeField(
        auto_now_add=True,
    )
    updated: Final[DateTimeField] = DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering: Final[list[str]] = ['name']

    def __str__(self) -> str:
        return self.name


class LoginCredential(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(
        User, on_delete=CASCADE, related_name='credentials'
    )
    name: CharField = CharField(
        verbose_name="Webisite's identifier",
        max_length=40,
        validators=(MaxLengthValidator(40),),
    )
    service: Final[ForeignKey] = ForeignKey(
        Service,
        on_delete=SET(set_service_other),
        related_name='credentials',
        db_column='id_service',
    )
    third_party_login: BooleanField = BooleanField()
    third_party_login_name: EncryptedCharField = EncryptedCharField(
        validators=(MaxLengthValidator(40),),
    )
    login: EncryptedCharField = EncryptedCharField(
        validators=(MaxLengthValidator(200),),
    )
    password: EncryptedCharField = EncryptedCharField(
        validators=(MaxLengthValidator(200),),
    )
    note: EncryptedTextField = EncryptedTextField(
        max_length=128,
        blank=True,
        null=True,
        validators=(MaxLengthValidator(128),),
    )
    slug: Final[SlugField] = SlugField(
        max_length=128, validators=(MaxLengthValidator(128),)
    )
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
    updated: Final[DateTimeField] = DateTimeField(auto_now=True)

    class Meta:
        ordering: Final[list[str]] = ['-created']

    def __str__(self) -> str:
        return f'{self.owner.username} | {self.service.name} | {self.name}'

    def validate_constraints(self, exclude: Any = None) -> None:
        super().validate_constraints(exclude)

        if (
            (self.third_party_login and self.third_party_login_name == '-----')
            or (
                not self.third_party_login
                and (self.login == '-----' or self.password == '-----')
            )
            or self.slug != slugify(f'{self.service.name} {self.name}')
        ):
            raise ValidationError('Slug')

    def get_absolute_url(self) -> str:
        return reverse('secret:credential_detail_view', args=(self.slug,))
