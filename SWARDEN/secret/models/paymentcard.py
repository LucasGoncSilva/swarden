from datetime import datetime
from typing import Any, Final
from uuid import uuid4

from account.models import User
from crypt.fields import EncryptedCharField, EncryptedTextField
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import (
    CASCADE,
    SET,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    SlugField,
    UUIDField,
)
from django.urls import reverse
from django.utils.text import slugify

from secret.month.models import MonthField


def set_card_type_other() -> UUIDField:
    return CardType.objects.get_or_create(name='Other')[0].pk


def set_bank_other() -> UUIDField:
    return CardType.objects.get_or_create(name='Other')[0].pk


def set_brand_other() -> UUIDField:
    return CardType.objects.get_or_create(name='Other')[0].pk


def get_today_year_month() -> str:
    today: datetime = datetime.today()
    return f'{today.year}-{today.month}'


class Brand(Model):
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
        ordering: Final[tuple[str]] = ('name',)

    def __str__(self) -> str:
        return self.name


class Bank(Model):
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
        ordering: Final[tuple[str]] = ('name',)

    def __str__(self) -> str:
        return self.name


class CardType(Model):
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
        ordering: Final[tuple[str]] = ('name',)

    def __str__(self) -> str:
        return self.name


class PaymentCard(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE, related_name='cards')
    name: EncryptedCharField = EncryptedCharField(
        verbose_name="Webisite's identifier",
        validators=(MaxLengthValidator(40),),
    )
    owners_name: EncryptedCharField = EncryptedCharField(
        validators=(MaxLengthValidator(64),),
    )
    card_type: Final[ForeignKey] = ForeignKey(
        CardType,
        on_delete=SET(set_card_type_other),
        related_name='cards',
        db_column='id_card_type',
    )
    number: EncryptedCharField = EncryptedCharField(
        validators=(MinLengthValidator(12), MaxLengthValidator(19)),
    )
    expiration = MonthField(default=get_today_year_month)
    cvv: EncryptedCharField = EncryptedCharField(
        validators=(
            MinLengthValidator(3),
            MaxLengthValidator(4),
        ),
    )
    bank: Final[ForeignKey] = ForeignKey(
        Bank, on_delete=SET(set_bank_other), related_name='cards', db_column='id_bank'
    )
    brand: Final[ForeignKey] = ForeignKey(
        Brand,
        on_delete=SET(set_brand_other),
        related_name='cards',
        db_column='id_brand',
    )
    branch: EncryptedCharField = EncryptedCharField(
        validators=(MinLengthValidator(3), MaxLengthValidator(11))
    )
    account: EncryptedCharField = EncryptedCharField(
        validators=(MinLengthValidator(3), MaxLengthValidator(11))
    )
    password: EncryptedCharField = EncryptedCharField(
        validators=(MinLengthValidator(4), MaxLengthValidator(6))
    )
    note: EncryptedTextField = EncryptedTextField(
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
        ordering: Final[tuple[str]] = ('-created',)

    def __str__(self) -> str:
        return f'{self.owner.username} | {self.card_type.name} | {self.name}'

    def validate_constraints(self, exclude: Any = None) -> None:
        super().validate_constraints(exclude)

        if self.slug != (expected_slug := slugify(f'{self.bank.name} {self.name}')):
            raise ValidationError(
                f'Expected slug to be {expected_slug}, found {self.slug}'
            )

    def get_absolute_url(self) -> str:
        return reverse('secret:card_detail_view', args=(self.slug,))
