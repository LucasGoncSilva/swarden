# File: `0001_initial.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.account.migrations`

No file docstring provided.

---

## Imports

### `#!py import django.core.validators`

Path: `#!py None`

Category: trdparty

??? example "Snippet"

    ```py
    import django.core.validators
    ```

### `#!py import django.db.models.deletion`

Path: `#!py None`

Category: trdparty

??? example "Snippet"

    ```py
    import django.db.models.deletion
    ```

### `#!py import uuid`

Path: `#!py None`

Category: native

??? example "Snippet"

    ```py
    import uuid
    ```

### `#!py import settings`

Path: `#!py django.conf`

Category: trdparty

??? example "Snippet"

    ```py
    from django.conf import settings
    ```

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
        dependencies = [('auth', '0012_alter_user_first_name_max_length')]
        operations = [migrations.CreateModel(name='User', fields=[('password', models.CharField(max_length=128, verbose_name='password')), ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')), ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')), ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)), ('username', models.CharField(max_length=20, unique=True)), ('is_staff', models.BooleanField(default=False)), ('is_active', models.BooleanField(default=False)), ('created', models.DateTimeField(auto_now_add=True)), ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')), ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'))], options={'abstract': False}), migrations.CreateModel(name='ActivationAccountToken', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)), ('value', models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(64), django.core.validators.MaxLengthValidator(64)])), ('used', models.BooleanField(default=False)), ('created', models.DateTimeField(auto_now_add=True)), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))])]
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
