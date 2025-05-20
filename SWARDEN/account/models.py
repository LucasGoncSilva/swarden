from datetime import datetime
from typing import Any, Final, Self
from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Model,
    UUIDField,
)


class sWardenUserManager(BaseUserManager):
    def create_user(
        self: Self, email: str, passphrase=None, **extra_fields: Any
    ) -> Self:
        if not email:
            raise ValueError('Email is required.')

        normalized_email: str = self.normalize_email(email)
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(passphrase)
        user.save(using=self._db)
        return user

    def create_superuser(self: Self, email, passphrase=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, passphrase, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username: Final[CharField] = CharField(max_length=150, unique=True)
    email: Final[EmailField] = EmailField(unique=True)
    is_active: bool | BooleanField = BooleanField(default=False)
    is_staff: Final[BooleanField] = BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = sWardenUserManager()

    def __str__(self: Self) -> str:
        return self.username


class ActivationAccountToken(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    user: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE)
    value: Final[CharField] = CharField(
        max_length=64, validators=[MinLengthValidator(64), MaxLengthValidator(64)]
    )
    used: BooleanField = BooleanField(default=False)
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    def __str__(self: Self) -> str:
        return f'{self.value}'

    def is_valid(self: Self) -> bool:
        if (
            self.value
            and len(self.value) == 64
            and isinstance(self.used, bool)
            and self.created
            and isinstance(self.created, datetime)
        ):
            return True
        return False
