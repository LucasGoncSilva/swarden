
# File: `models.py`
Path: `SWARDEN.honeypot`



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

### `#!py import MaxLengthValidator`

Path: `#!py django.core.validators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.validators import MaxLengthValidator
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

### `#!py IP`

Type: `#!py Final[CharField]`

Value: `#!py CharField(max_length=64, validators=[MaxLengthValidator(64)])`

??? example "SNIPPET"

    ```py
    IP: Final[CharField] = CharField(max_length=64, validators=[MaxLengthValidator(64)])
    ```

### `#!py URL`

Type: `#!py Final[CharField]`

Value: `#!py CharField(max_length=256, validators=[MaxLengthValidator(256)])`

??? example "SNIPPET"

    ```py
    URL: Final[CharField] = CharField(max_length=256, validators=[MaxLengthValidator(256)])
    ```



---

## Classes

### `#!py class Attempt`

Parents: `Model`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Attempt(Model):
        id: Final[UUIDField] = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
        IP: Final[CharField] = CharField(max_length=64, validators=[MaxLengthValidator(64)])
        username: Final[CharField] = CharField(max_length=256, verbose_name='Nome de Usuário', validators=[MaxLengthValidator(256)], blank=True, null=True)
        password: Final[CharField] = CharField(max_length=256, verbose_name='Senha', validators=[MaxLengthValidator(256)], blank=True, null=True)
        URL: Final[CharField] = CharField(max_length=256, validators=[MaxLengthValidator(256)])
        timestamp: Final[DateTimeField] = DateTimeField(auto_now_add=True, verbose_name='Data e Hora')

        class Meta:
            verbose_name: Final[str] = 'Registro'
            verbose_name_plural: Final[str] = 'Registros'

        def __str__(self) -> str:
            date: datetime = self.timestamp
            d: int = date.day
            m: int = date.month
            y: int = date.year
            h: int = date.hour
            min: int = date.minute
            s: int = date.second
            return f'{self.pk}: {d}/{m}/{y} ({h}h{min}m{s}s) UTC+3'

        def is_valid(self) -> bool:
            if self.IP and len(self.IP) <= 64 and self.username and (len(self.username) <= 256) and self.password and (len(self.password) <= 256) and self.URL and (len(self.URL) <= 256) and self.timestamp and isinstance(self.timestamp, datetime):
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
        verbose_name: Final[str] = 'Registro'
        verbose_name_plural: Final[str] = 'Registros'
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
        date: datetime = self.timestamp
        d: int = date.day
        m: int = date.month
        y: int = date.year
        h: int = date.hour
        min: int = date.minute
        s: int = date.second
        return f'{self.pk}: {d}/{m}/{y} ({h}h{min}m{s}s) UTC+3'
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
        if self.IP and len(self.IP) <= 64 and self.username and (len(self.username) <= 256) and self.password and (len(self.password) <= 256) and self.URL and (len(self.URL) <= 256) and self.timestamp and isinstance(self.timestamp, datetime):
            return True
        return False
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
