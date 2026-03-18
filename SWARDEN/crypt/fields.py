from typing import Any, Self, cast

from django.conf import settings
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import CharField, TextField
from django.db.models.expressions import Expression

from crypt.algo import sWardenCryptography


class EncryptedFieldMixin:
    def __init__(
        self,
        *args: Any,
        master_key: str = settings.CRYPTOGRAPHY_KEY,
        pepper_field: str = settings.SYSTEM_PEPPER,
        **kwargs: Any,
    ) -> None:
        self.master_key: str = master_key
        self.pepper_field: str = pepper_field

        return super().__init__(*args, **kwargs)

    def get_prep_value(self, value: Any) -> str:
        if value:
            return sWardenCryptography.encrypt(
                str(value), self.master_key, self.pepper_field
            )
        return value

    def from_db_value(
        self, value: Any, expression: Expression, connection: BaseDatabaseWrapper
    ) -> str:
        if value:
            return sWardenCryptography.decrypt(
                str(value), self.master_key, self.pepper_field
            )
        return value


class EncryptedCharField(EncryptedFieldMixin, CharField):
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        return cast(Self, super().__new__(cls))


class EncryptedTextField(EncryptedFieldMixin, TextField):
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        return cast(Self, super().__new__(cls))
