
# File: `0001_initial.py`
Path: `SWARDEN.account.migrations`



---

## Imports

### `#!py import django.contrib.auth.models`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import django.contrib.auth.models
    ```

### `#!py import django.contrib.auth.validators`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import django.contrib.auth.validators
    ```

### `#!py import django.core.validators`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import django.core.validators
    ```

### `#!py import django.db.models.deletion`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import django.db.models.deletion
    ```

### `#!py import django.utils.timezone`

Path: `#!py None`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    import django.utils.timezone
    ```

### `#!py import uuid`

Path: `#!py None`

Category: Native

??? example "SNIPPET"

    ```py
    import uuid
    ```

### `#!py import settings`

Path: `#!py django.conf`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.conf import settings
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
        dependencies = [('auth', '0012_alter_user_first_name_max_length')]
        operations = [migrations.CreateModel(name='User', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('password', models.CharField(max_length=128, verbose_name='password')), ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')), ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')), ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')), ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')), ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')), ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')), ('first_name', models.CharField(blank=True, max_length=150, verbose_name='Nome')), ('last_name', models.CharField(blank=True, max_length=150, verbose_name='Sobrenome')), ('email', models.EmailField(max_length=254, unique=True)), ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')), ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'))], options={'verbose_name': 'user', 'verbose_name_plural': 'users', 'abstract': False}, managers=[('objects', django.contrib.auth.models.UserManager())]), migrations.CreateModel(name='ActivationAccountToken', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)), ('value', models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(64), django.core.validators.MaxLengthValidator(64)])), ('used', models.BooleanField(default=False, verbose_name='Usado?')), ('created', models.DateTimeField(auto_now_add=True)), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'Token de Ativação', 'verbose_name_plural': 'Tokens de Ativação'})]
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
