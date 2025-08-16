# File: `admin.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.account`

No file docstring provided.

---

## Imports

### `#!py import ModelAdmin`

Path: `#!py django.contrib.admin`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.admin import ModelAdmin
    ```

### `#!py import site`

Path: `#!py django.contrib.admin`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.admin import site
    ```

### `#!py import UserAdmin`

Path: `#!py django.contrib.auth.admin`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.admin import UserAdmin
    ```

### `#!py import UserChangeForm`

Path: `#!py account.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from account.forms import UserChangeForm
    ```

### `#!py import UserCreationForm`

Path: `#!py account.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from account.forms import UserCreationForm
    ```

### `#!py import ActivationAccountToken`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import ActivationAccountToken
    ```

### `#!py import User`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import User
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class UserAdmin`

Parents: `BaseUserAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class UserAdmin(BaseUserAdmin):
        form = UserChangeForm
        add_form = UserCreationForm
        list_display = ('username', 'is_active', 'is_staff', 'created')
        search_fields = ('username',)
        readonly_fields = ('created',)
        fieldsets = ((None, {'fields': ('username', 'password')}), ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), ('Important dates', {'fields': ('last_login', 'created')}))
        add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2')}),)
        ordering = ('username',)
    ```

### `#!py class ActivationAccountTokenAdmin`

Parents: `ModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class ActivationAccountTokenAdmin(ModelAdmin):
        list_filter = ('user__is_active',)
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
