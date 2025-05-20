from typing import Final
from uuid import uuid4

from account.models import User
from django.core.validators import MaxLengthValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    SlugField,
    TextField,
    UUIDField,
)
from django.template.defaultfilters import slugify
from django.urls import reverse
from utils import xor

from secret.choices import credentials_services


class LoginCredential(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(
        User, on_delete=CASCADE, related_name='credentials'
    )
    service: CharField = CharField(
        max_length=64,
        choices=credentials_services,
        validators=[MaxLengthValidator(64)],
    )
    name: CharField = CharField(
        max_length=40,
        validators=[MaxLengthValidator(40)],
    )
    third_party_login: BooleanField = BooleanField()
    third_party_login_name: CharField = CharField(
        max_length=40,
        validators=[MaxLengthValidator(40)],
    )
    login: CharField = CharField(max_length=200, validators=[MaxLengthValidator(200)])
    password: CharField = CharField(
        max_length=200, validators=[MaxLengthValidator(200)]
    )
    note: TextField = TextField(
        max_length=128,
        blank=True,
        null=True,
        validators=[MaxLengthValidator(128)],
    )
    slug: Final[SlugField] = SlugField(
        max_length=128, validators=[MaxLengthValidator(128)]
    )
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
    updated: Final[DateTimeField] = DateTimeField(auto_now=True)

    class Meta:
        ordering: Final[list[str]] = ['-created']

    def __str__(self) -> str:
        return f'{str(self.owner.username)} | {self.service} | {self.name}'

    def get_absolute_url(self) -> str:
        return reverse('secret:credential_list_view')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.third_party_login_name = xor(
            str(self.third_party_login_name), self.owner.password[21:]
        )
        self.login = xor(str(self.login), self.owner.password[21:])
        self.password = xor(str(self.password), self.owner.password[21:])
        self.note = xor(str(self.note), self.owner.password[21:])

        return super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    @classmethod
    def from_db(cls, db, field_names, values):
        cred: LoginCredential = super().from_db(db, field_names, values)

        cred.third_party_login_name = xor(
            str(cred.third_party_login_name), cred.owner.password[21:], encrypt=False
        )
        cred.login = xor(str(cred.login), cred.owner.password[21:], encrypt=False)
        cred.password = xor(str(cred.password), cred.owner.password[21:], encrypt=False)
        cred.note = xor(str(cred.note), cred.owner.password[21:], encrypt=False)

        return cred

    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {
            'service': 64,
            'name': 40,
            'slug': 128,
            'third_party_login_name': 40,
            'login': 200,
            'password': 200,
        }

        return max_length[var]

    def check_field_length(self, var: str) -> bool:
        value = self.__getattribute__(var)

        return len(value) <= self.expected_max_length(var)

    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = [
            'service',
            'name',
            'slug',
            'third_party_login_name',
            'login',
            'password',
        ]

        return all(map(self.check_field_length, vars))

    def all_fields_present(self) -> bool:
        if (
            self.owner
            and self.name
            and self.service in [slug for slug, _ in credentials_services]
            and self.slug == f'{self.service}{slugify(str(self.name))}'
            and self.third_party_login_name
            and self.login
            and self.password
        ):
            if (self.third_party_login and self.third_party_login_name != '-----') or (
                not self.third_party_login
                and self.login != '-----'
                and self.password != '-----'
            ):
                return True
        return False

    def all_fields_of_correct_types(self) -> bool:
        return [
            str(type(self.owner)),
            type(self.service),
            type(self.name),
            type(self.slug),
            type(self.third_party_login),
            type(self.third_party_login_name),
            type(self.login),
            type(self.password),
        ] == [
            "<class 'account.models.User'>",
            str,
            str,
            str,
            bool,
            str,
            str,
            str,
        ]

    def is_valid(self) -> bool:
        if (
            self.all_fields_present()
            and self.all_fields_of_correct_types()
            and self.all_fields_of_right_length()
        ):
            return True
        return False
