
# File: `models.py`
Path: `SWARDEN.account`



---

## Imports

### `#!py import datetime`

Path: `#!py datetime`

Category: Native

??? example "SNIPPET"

    ```py
    from datetime import datetime
    ```

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import uuid4`

Path: `#!py uuid`

Category: Native

??? example "SNIPPET"

    ```py
    from uuid import uuid4
    ```

### `#!py import AbstractUser`

Path: `#!py django.contrib.auth.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth.models import AbstractUser
    ```

### `#!py import MaxLengthValidator`

Path: `#!py django.core.validators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.validators import MaxLengthValidator
    ```

### `#!py import MinLengthValidator`

Path: `#!py django.core.validators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.validators import MinLengthValidator
    ```

### `#!py import CASCADE`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import CASCADE
    ```

### `#!py import BooleanField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import BooleanField
    ```

### `#!py import CharField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import CharField
    ```

### `#!py import DateTimeField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import DateTimeField
    ```

### `#!py import EmailField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import EmailField
    ```

### `#!py import ForeignKey`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import ForeignKey
    ```

### `#!py import Model`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import Model
    ```

### `#!py import UUIDField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import UUIDField
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class User`

Parents: `AbstractUser`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class User(AbstractUser):
        first_name: Final[CharField] = CharField(max_length=150, blank=True, verbose_name='Nome')
        last_name: Final[CharField] = CharField(max_length=150, blank=True, verbose_name='Sobrenome')
        email: Final[EmailField] = EmailField(unique=True)
    ```

### `#!py class ActivationAccountToken`

Parents: `Model`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class ActivationAccountToken(Model):
        id: Final[UUIDField] = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
        user: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE)
        value: Final[CharField] = CharField(max_length=64, validators=[MinLengthValidator(64), MaxLengthValidator(64)])
        used: BooleanField = BooleanField(default=False, verbose_name='Usado?')
        created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

        class Meta:
            verbose_name: Final[str] = 'Token de Ativação'
            verbose_name_plural: Final[str] = 'Tokens de Ativação'

        def __str__(self) -> str:
            return f'{self.value}'

        def is_valid(self) -> bool:
            if self.value and len(self.value) == 64 and isinstance(self.used, bool) and self.created and isinstance(self.created, datetime):
                return True
            return False
    ```

### `#!py class Meta`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Meta:
        verbose_name: Final[str] = 'Token de Ativação'
        verbose_name_plural: Final[str] = 'Tokens de Ativação'
    ```



---

## Functions

### `#!py def __str__`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def __str__(self) -> str:
        return f'{self.value}'
    ```

### `#!py def is_valid`

Type: `#!py ...`

Return Type: `#!py bool`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def is_valid(self) -> bool:
        if self.value and len(self.value) == 64 and isinstance(self.used, bool) and self.created and isinstance(self.created, datetime):
            return True
        return False
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
