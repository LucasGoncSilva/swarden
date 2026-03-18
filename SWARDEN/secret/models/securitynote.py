from typing import Any, Final
from uuid import uuid4

from account.models import User
from crypt.fields import EncryptedTextField
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
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


def set_note_type_other() -> UUIDField:
    return NoteType.objects.get_or_create(name='Other')[0].pk


class NoteType(Model):
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


class SecurityNote(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='notes',
    )
    title: Final[CharField] = CharField(
        max_length=40, validators=(MaxLengthValidator(40),)
    )
    content: EncryptedTextField = EncryptedTextField(
        validators=(MaxLengthValidator(1000),)
    )
    note_type: Final[ForeignKey] = ForeignKey(
        NoteType,
        on_delete=SET(set_note_type_other),
        related_name='credentials',
        db_column='id_note_type',
    )
    slug: Final[SlugField] = SlugField(
        max_length=50, validators=(MaxLengthValidator(50),)
    )
    created: Final[DateTimeField] = DateTimeField(
        auto_now_add=True,
    )
    updated: Final[DateTimeField] = DateTimeField(
        auto_now=True,
    )

    def __str__(self) -> str:
        return f'{self.owner.username} | {self.title}'

    def validate_constraints(self, exclude: Any = None) -> None:
        super().validate_constraints(exclude)

        if self.slug != slugify(self.title):
            raise ValidationError('Slug')

    def get_absolute_url(self) -> str:
        return reverse('secret:note_detail_view', args=(self.slug,))
