from __future__ import annotations

from hashlib import sha256
from typing import Any, Final
from unicodedata import normalize
from uuid import uuid4

from crypt.fields import EncryptedCharField
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    AnonymousUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    OneToOneField,
    UUIDField,
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


ARGON2_REGEX = RegexValidator(
    r'^argon2\$argon2id.*$', 'Only Argon2 hash is allowed.', code='invalid_argon2_hash'
)


class sWardenUserManager(BaseUserManager):  # pragma: no cover
    def create_user(
        self, username: str, password: str | None = None, **extra_fields: Any
    ) -> User:
        if not username:
            raise ValueError('Username is required.')

        user: User = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username: str, password: str | None = None, **extra_fields
    ) -> User:
        if settings.IS_DEV_ENVIRONMENT:
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_active', True)
            return self.create_user(username, password, **extra_fields)

        raise PermissionError('This environ cannot proceed with this operation.')


class User(AbstractBaseUser, PermissionsMixin):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    username: Final[CharField] = CharField(max_length=20, unique=True)
    address: Final[UUIDField] = UUIDField(default=uuid4, unique=True, editable=False)
    is_staff: Final[BooleanField] = BooleanField(default=False)
    is_active: BooleanField | bool = BooleanField(default=False)
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    USERNAME_FIELD: Final[str] = 'username'

    objects: sWardenUserManager = sWardenUserManager()

    def __str__(self) -> str:
        return self.username

    @property
    def pk_uidb64(self) -> str:
        return urlsafe_base64_encode(force_bytes(self.pk))


class ActivationAccountToken(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    user: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE)
    value: Final[CharField] = CharField(
        max_length=64, validators=(MinLengthValidator(64), MaxLengthValidator(64))
    )
    used: BooleanField = BooleanField(default=False)
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def create_activation_account_token(user: User) -> ActivationAccountToken:
        token_hash: str = sha256(f'{user.username}{user.password}'.encode()).hexdigest()

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value=token_hash,
            user=user,
            used=False,
        )

        token.full_clean()

        return token


class RecoveryPhrase(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    user: Final[OneToOneField[User]] = OneToOneField(User, on_delete=CASCADE)
    phrase_hash: EncryptedCharField = EncryptedCharField(validators=(ARGON2_REGEX,))
    fingerprint: CharField = CharField(
        max_length=64, db_index=True, unique=True, validators=(MinLengthValidator(64),)
    )
    is_active: Final[BooleanField] = BooleanField(default=False)
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} | {self.fingerprint}'

    @staticmethod
    def generate_fingerprint(phrase: str) -> str:
        return sha256(
            ' '.join(normalize('NFKD', phrase.lower().strip())).encode()
        ).hexdigest()

    @staticmethod
    def create_user_recovery(user: AbstractBaseUser | AnonymousUser) -> str:
        if RecoveryPhrase.objects.filter(user=user, is_active=True).count() > 0:
            raise PermissionError('This user already have a 12-words recovery list.')

        recovery, _ = RecoveryPhrase.objects.get_or_create(user=user)

        words: str = settings.MNEMONIC.generate(strength=128)

        recovery.set_phrase(words)
        recovery.full_clean()
        recovery.save()

        return words

    def set_phrase(self, phrase: str) -> None:
        self.phrase_hash = make_password(phrase)
        self.fingerprint = self.generate_fingerprint(phrase)

    def is_valid_phrase(self, phrase: str) -> bool:
        return check_password(phrase, self.phrase_hash)
