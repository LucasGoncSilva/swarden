# File: `0001_initial.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.mail.migrations`

No file docstring provided.

---

## Imports

### `#!py import migrations`

Path: `#!py django.db`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db import migrations
    ```

### `#!py import models`

Path: `#!py django.db`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db import models
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class Migration`

Parents: `None`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class Migration(migrations.Migration):
        initial = True
        dependencies = []
        operations = [migrations.CreateModel(name='WakeDatabase', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('created', models.DateField(auto_created=True, auto_now_add=True))])]
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
