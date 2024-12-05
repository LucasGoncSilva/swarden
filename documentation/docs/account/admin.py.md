
# File: `admin.py`
Path: `SWARDEN.account`



---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import Type`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Type
    ```

### `#!py import swarden_admin`

Path: `#!py CORE.admin`

Category: Local

??? example "SNIPPET"

    ```py
    from CORE.admin import swarden_admin
    ```

### `#!py import ModelAdmin`

Path: `#!py django.contrib.admin`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.admin import ModelAdmin
    ```

### `#!py import admin`

Path: `#!py django.contrib.auth`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth import admin
    ```

### `#!py import UserChangeForm`

Path: `#!py account.forms`

Category: Local

??? example "SNIPPET"

    ```py
    from account.forms import UserChangeForm
    ```

### `#!py import UserCreationForm`

Path: `#!py account.forms`

Category: Local

??? example "SNIPPET"

    ```py
    from account.forms import UserCreationForm
    ```

### `#!py import ActivationAccountToken`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import ActivationAccountToken
    ```

### `#!py import User`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import User
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class UserAdmin`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class UserAdmin(auth_admin.UserAdmin):
        list_display: Final = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
        search_fields: Final = ('username', 'email', 'first_name', 'last_name')
        add_fieldsets: Final = ((None, {'classes': ('wide',), 'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')}),)
        form: Type[UserChangeForm] = UserChangeForm
        add_form: Type[UserCreationForm] = UserCreationForm
    ```

### `#!py class ActivationAccountTokenAdmin`

Parents: `ModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class ActivationAccountTokenAdmin(ModelAdmin):
        list_filter: Final = ('user__is_active',)
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
