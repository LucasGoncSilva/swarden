
# File: `0001_initial.py`
Path: `SWARDEN.honeypot.migrations`



---

## Imports

### `#!py import django.core.validators`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import django.core.validators
    ```

### `#!py import uuid`

Path: `#!py None`

Category: Native

??? example "SNIPPET"

    ```py
    import uuid
    ```

### `#!py import migrations`

Path: `#!py django.db`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db import migrations
    ```

### `#!py import models`

Path: `#!py django.db`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db import models
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class Migration`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Migration(migrations.Migration):
        initial = True
        dependencies = []
        operations = [migrations.CreateModel(name='Attempt', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)), ('IP', models.CharField(max_length=64, validators=[django.core.validators.MaxLengthValidator(64)])), ('username', models.CharField(blank=True, max_length=256, null=True, validators=[django.core.validators.MaxLengthValidator(256)], verbose_name='Nome de Usuário')), ('password', models.CharField(blank=True, max_length=256, null=True, validators=[django.core.validators.MaxLengthValidator(256)], verbose_name='Senha')), ('URL', models.CharField(max_length=256, validators=[django.core.validators.MaxLengthValidator(256)])), ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Data e Hora'))], options={'verbose_name': 'Registro', 'verbose_name_plural': 'Registros'})]
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
