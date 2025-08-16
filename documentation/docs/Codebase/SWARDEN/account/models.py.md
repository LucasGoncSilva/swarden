# File: `models.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.account`

No file docstring provided.

---

## Imports

### `#!py import datetime`

Path: `#!py datetime`

Category: native

??? example "Snippet"

    ```py
    from datetime import datetime
    ```

### `#!py import getenv`

Path: `#!py os`

Category: native

??? example "Snippet"

    ```py
    from os import getenv
    ```

### `#!py import Any`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Any
    ```

### `#!py import Final`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Final
    ```

### `#!py import Self`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Self
    ```

### `#!py import uuid4`

Path: `#!py uuid`

Category: native

??? example "Snippet"

    ```py
    from uuid import uuid4
    ```

### `#!py import AbstractBaseUser`

Path: `#!py django.contrib.auth.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.models import AbstractBaseUser
    ```

### `#!py import BaseUserManager`

Path: `#!py django.contrib.auth.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.models import BaseUserManager
    ```

### `#!py import PermissionsMixin`

Path: `#!py django.contrib.auth.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.models import PermissionsMixin
    ```

### `#!py import MaxLengthValidator`

Path: `#!py django.core.validators`

Category: trdparty

??? example "Snippet"

    ```py
    from django.core.validators import MaxLengthValidator
    ```

### `#!py import MinLengthValidator`

Path: `#!py django.core.validators`

Category: trdparty

??? example "Snippet"

    ```py
    from django.core.validators import MinLengthValidator
    ```

### `#!py import CASCADE`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import CASCADE
    ```

### `#!py import BooleanField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import BooleanField
    ```

### `#!py import CharField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import CharField
    ```

### `#!py import DateTimeField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import DateTimeField
    ```

### `#!py import ForeignKey`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import ForeignKey
    ```

### `#!py import Model`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import Model
    ```

### `#!py import UUIDField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import UUIDField
    ```



---

## Consts

### `#!py USERNAME_FIELD`

Type: `#!py Final[str]`

Value: `#!py 'username'`

??? example "Snippet"

    ```py
    USERNAME_FIELD: Final[str] = 'username'
    ```



---

## Classes

### `#!py class sWardenUserManager`

Parents: `BaseUserManager`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class sWardenUserManager(BaseUserManager):

        def create_user(self: Self, username: str, password: str | None=None, **extra_fields: Any) -> Self:
            if not username:
                raise ValueError('Username is required.')
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self: Self, username: str, password: str | None=None, **extra_fields) -> Self:
            if getenv('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev') == 'CORE.settings.dev':
                extra_fields.setdefault('is_staff', True)
                extra_fields.setdefault('is_superuser', True)
                extra_fields.setdefault('is_active', True)
                return self.create_user(username, password, **extra_fields)
            raise PermissionError('This environ cannot proceed with this operation.')
    ```

### `#!py class User`

Parents: `AbstractBaseUser, PermissionsMixin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class User(AbstractBaseUser, PermissionsMixin):
        id: Final[UUIDField] = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
        username: Final[CharField] = CharField(max_length=20, unique=True)
        is_staff: Final[BooleanField] = BooleanField(default=False)
        is_active: BooleanField | bool = BooleanField(default=False)
        created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
        USERNAME_FIELD: Final[str] = 'username'
        objects: sWardenUserManager = sWardenUserManager()

        def __str__(self: Self) -> str:
            return self.username
    ```

### `#!py class ActivationAccountToken`

Parents: `Model`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class ActivationAccountToken(Model):
        id: Final[UUIDField] = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
        user: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE)
        value: Final[CharField] = CharField(max_length=64, validators=[MinLengthValidator(64), MaxLengthValidator(64)])
        used: BooleanField = BooleanField(default=False)
        created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

        def __str__(self: Self) -> str:
            return f'{self.value}'

        def is_valid(self: Self) -> bool:
            if self.value and len(self.value) == 64 and isinstance(self.used, bool) and self.created and isinstance(self.created, datetime):
                return True
            return False
    ```



---

## Functions

### `#!py def create_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self, username: str, password: str | None`

Kwargs: `#!py None`

Return Type: `#!py Self`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def create_user(self: Self, username: str, password: str | None=None, **extra_fields: Any) -> Self:
        if not username:
            raise ValueError('Username is required.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    ```

### `#!py def create_superuser`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self, username: str, password: str | None`

Kwargs: `#!py None`

Return Type: `#!py Self`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def create_superuser(self: Self, username: str, password: str | None=None, **extra_fields) -> Self:
        if getenv('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev') == 'CORE.settings.dev':
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_active', True)
            return self.create_user(username, password, **extra_fields)
        raise PermissionError('This environ cannot proceed with this operation.')
    ```

### `#!py def __str__`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def __str__(self: Self) -> str:
        return self.username
    ```

### `#!py def __str__`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def __str__(self: Self) -> str:
        return f'{self.value}'
    ```

### `#!py def is_valid`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self`

Kwargs: `#!py None`

Return Type: `#!py bool`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def is_valid(self: Self) -> bool:
        if self.value and len(self.value) == 64 and isinstance(self.used, bool) and self.created and isinstance(self.created, datetime):
            return True
        return False
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
