from typing import Final
from uuid import uuid4

from django.core.validators import MaxLengthValidator, MinLengthValidator
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

from account.models import User
from secret.choices import cards_banks, cards_brands, cards_types, credentials_services
from secret.month.models import MonthField
from utils import xor


# Create your models here.
class LoginCredential(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(
        User, on_delete=CASCADE, related_name="credentials", verbose_name="Dono"
    )
    service: CharField = CharField(
        max_length=64,
        choices=credentials_services,
        verbose_name="Serviço",
        validators=[MaxLengthValidator(64)],
    )
    name: CharField = CharField(
        max_length=40,
        verbose_name="Apelido (ex: Conta Principal)",
        validators=[MaxLengthValidator(40)],
    )
    thirdy_party_login: BooleanField = BooleanField(
        verbose_name="Login com serviço de terceiro?"
    )
    thirdy_party_login_name: CharField = CharField(
        max_length=40,
        verbose_name="Apelido do serviço de terceiro",
        validators=[MaxLengthValidator(40)],
    )
    login: CharField = CharField(
        max_length=200, verbose_name="Login", validators=[MaxLengthValidator(200)]
    )
    password: CharField = CharField(
        max_length=200, verbose_name="Senha", validators=[MaxLengthValidator(200)]
    )
    note: TextField = TextField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="Anotação particular",
        validators=[MaxLengthValidator(128)],
    )
    slug: Final[SlugField] = SlugField(
        max_length=128, validators=[MaxLengthValidator(128)]
    )
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
    updated: Final[DateTimeField] = DateTimeField(auto_now=True)

    class Meta:
        ordering: Final[list[str]] = ["-created"]
        verbose_name: Final[str] = "Credencial"
        verbose_name_plural: Final[str] = "Credenciais"

    def __str__(self) -> str:
        return f"{str(self.owner.username)} | {self.service} | {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("secret:credential_list_view")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.thirdy_party_login_name = xor(
            str(self.thirdy_party_login_name), self.owner.password[21:]
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

        cred.thirdy_party_login_name = xor(
            str(cred.thirdy_party_login_name), cred.owner.password[21:], encrypt=False
        )
        cred.login = xor(str(cred.login), cred.owner.password[21:], encrypt=False)
        cred.password = xor(str(cred.password), cred.owner.password[21:], encrypt=False)
        cred.note = xor(str(cred.note), cred.owner.password[21:], encrypt=False)

        return cred

    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {
            "service": 64,
            "name": 40,
            "slug": 128,
            "thirdy_party_login_name": 40,
            "login": 200,
            "password": 200,
        }

        return max_length[var]

    def check_field_length(self, var: str) -> bool:
        value = self.__getattribute__(var)

        return len(value) <= self.expected_max_length(var)

    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = [
            "service",
            "name",
            "slug",
            "thirdy_party_login_name",
            "login",
            "password",
        ]

        return all(map(self.check_field_length, vars))

    def all_fields_present(self) -> bool:
        if (
            self.owner
            and self.name
            and self.service in [slug for slug, _ in credentials_services]
            and self.slug == f"{self.service}{slugify(str(self.name))}"
            and self.thirdy_party_login_name
            and self.login
            and self.password
        ):
            if (
                self.thirdy_party_login and self.thirdy_party_login_name != "-----"
            ) or (
                not self.thirdy_party_login
                and self.login != "-----"
                and self.password != "-----"
            ):
                return True
        return False

    def all_fields_of_correct_types(self) -> bool:
        return [
            str(type(self.owner)),
            type(self.service),
            type(self.name),
            type(self.slug),
            type(self.thirdy_party_login),
            type(self.thirdy_party_login_name),
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


class Card(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(
        User, on_delete=CASCADE, related_name="cards", verbose_name="Dono"
    )
    name: CharField = CharField(
        max_length=40,
        verbose_name="Apelido (ex: Cartão da Família)",
        validators=[MaxLengthValidator(40)],
    )
    card_type: CharField = CharField(
        max_length=4,
        choices=cards_types,
        verbose_name="Tipo (débito, crédito, ...)",
        validators=[MaxLengthValidator(4)],
    )
    number: CharField = CharField(
        max_length=19,
        validators=[MinLengthValidator(12), MaxLengthValidator(19)],
        verbose_name="Número do Cartão",
    )
    expiration = MonthField(verbose_name="Data de Expiração")
    cvv: CharField = CharField(
        max_length=4,
        validators=[MinLengthValidator(3), MaxLengthValidator(4)],
        verbose_name="cvv",
    )
    bank: CharField = CharField(
        max_length=64, choices=cards_banks, verbose_name="Banco"
    )
    brand: CharField = CharField(
        max_length=64, choices=cards_brands, verbose_name="Bandeira"
    )
    owners_name: CharField = CharField(
        max_length=64,
        verbose_name="Nome do Titular (como no cartão)",
        validators=[MaxLengthValidator(64)],
    )
    note: TextField = TextField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="Anotação Particular",
        validators=[MaxLengthValidator(128)],
    )
    slug: Final[SlugField] = SlugField(
        max_length=128, validators=[MaxLengthValidator(128)]
    )
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
    updated: Final[DateTimeField] = DateTimeField(auto_now=True)

    class Meta:
        ordering: Final[list[str]] = ["-created"]
        verbose_name: Final[str] = "Cartão"
        verbose_name_plural: Final[str] = "Cartões"

    def __str__(self) -> str:
        return f"{str(self.owner.username)} | {self.card_type} | {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("secret:card_list_view")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.name = xor(str(self.name), self.owner.password[21:])
        self.card_type = xor(str(self.card_type), self.owner.password[21:])
        self.number = xor(str(self.number), self.owner.password[21:])
        self.cvv = xor(str(self.cvv), self.owner.password[21:])
        self.bank = xor(str(self.bank), self.owner.password[21:])
        self.brand = xor(str(self.brand), self.owner.password[21:])
        self.owners_name = xor(str(self.owners_name), self.owner.password[21:])
        self.note = xor(str(self.note), self.owner.password[21:])

        return super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    @classmethod
    def from_db(cls, db, field_names, values):
        card: Card = super().from_db(db, field_names, values)

        card.name = xor(str(card.name), card.owner.password[21:], encrypt=False)
        card.card_type = xor(
            str(card.card_type), card.owner.password[21:], encrypt=False
        )
        card.number = xor(str(card.number), card.owner.password[21:], encrypt=False)
        card.cvv = xor(str(card.cvv), card.owner.password[21:], encrypt=False)
        card.bank = xor(str(card.bank), card.owner.password[21:], encrypt=False)
        card.brand = xor(str(card.brand), card.owner.password[21:], encrypt=False)
        card.owners_name = xor(
            str(card.owners_name), card.owner.password[21:], encrypt=False
        )
        card.note = xor(str(card.note), card.owner.password[21:], encrypt=False)

        return card

    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {
            "name": 40,
            "card_type": 16,
            "number": 19,
            "cvv": 4,
            "bank": 64,
            "brand": 64,
            "slug": 128,
            "owners_name": 64,
            "note": 128,
        }

        return max_length[var]

    def expected_min_length(self, var: str) -> int:
        min_length: Final[dict[str, int]] = {
            "number": 12,
            "cvv": 3,
        }

        return min_length[var]

    def check_field_length(self, var: str) -> bool:
        if var == "expiration":
            return True

        value = self.__getattribute__(var)

        if var in ["number", "cvv"]:
            return (
                self.expected_min_length(var)
                <= len(value)
                <= self.expected_max_length(var)
            )

        return len(value) <= self.expected_max_length(var)

    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = [
            "name",
            "card_type",
            "number",
            "expiration",
            "cvv",
            "bank",
            "brand",
            "slug",
            "owners_name",
        ]

        return all(map(self.check_field_length, vars))

    def all_fields_present(self) -> bool:
        return bool(
            self.owner
            and self.name
            and self.card_type in [slug for slug, _ in cards_types]
            and self.number
            and self.expiration
            and self.cvv
            and self.bank in [slug for slug, _ in cards_banks]
            and self.brand in [slug for slug, _ in cards_brands]
            and self.owners_name
            and self.slug == f"{self.bank}{slugify(str(self.name))}"
        )

    def all_fields_of_correct_types(self) -> bool:
        return [
            str(type(self.owner)),
            type(self.name),
            type(self.card_type),
            type(self.number),
            str(type(self.expiration)),
            type(self.cvv),
            type(self.bank),
            type(self.brand),
            type(self.slug),
            type(self.owners_name),
        ] == [
            "<class 'account.models.User'>",
            str,
            str,
            str,
            "<class 'secret.month.Month'>",
            str,
            str,
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


class SecurityNote(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(
        User, on_delete=CASCADE, related_name="notes", verbose_name="Dono"
    )
    title: Final[CharField] = CharField(
        max_length=40, verbose_name="Título", validators=[MaxLengthValidator(40)]
    )
    content: TextField = TextField(
        max_length=300, verbose_name="Conteúdo", validators=[MaxLengthValidator(300)]
    )
    slug: Final[SlugField] = SlugField(
        max_length=50, validators=[MaxLengthValidator(50)]
    )
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
    updated: Final[DateTimeField] = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{str(self.owner.username)} | {self.title}"

    def get_absolute_url(self) -> str:
        return reverse("secret:note_list_view")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.content = xor(str(self.content), self.owner.password[21:])

        return super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    @classmethod
    def from_db(cls, db, field_names, values):
        note: SecurityNote = super().from_db(db, field_names, values)
        note.content = xor(str(note.content), note.owner.password[21:], encrypt=False)
        return note

    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {
            "title": 40,
            "content": 300,
            "slug": 50,
        }

        return max_length[var]

    def check_field_length(self, var: str) -> bool:
        value = self.__getattribute__(var)

        return len(value) <= self.expected_max_length(var)

    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = [
            "title",
            "content",
            "slug",
        ]

        return all(map(self.check_field_length, vars))

    def all_fields_present(self) -> bool:
        return bool(
            self.owner
            and self.title
            and self.content
            and self.slug == slugify(str(self.title))
        )

    def all_fields_of_correct_types(self) -> bool:
        return [
            str(type(self.owner)),
            type(self.title),
            type(self.content),
            type(self.slug),
        ] == [
            "<class 'account.models.User'>",
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

    class Meta:
        ordering: Final[list[str]] = ["-created"]
        verbose_name: Final[str] = "Nota de Segurança"
        verbose_name_plural: Final[str] = "Notas de Segurança"
