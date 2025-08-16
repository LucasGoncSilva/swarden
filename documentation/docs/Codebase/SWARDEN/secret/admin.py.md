# File: `admin.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.secret`

No file docstring provided.

---

## Imports

### `#!py import Any`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Any
    ```

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

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import PaymentCard`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import PaymentCard
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import SecurityNote
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class BasesWardenModelAdmin`

Parents: `ModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class BasesWardenModelAdmin(ModelAdmin):
        exclude: tuple = tuple()
        _exclude: tuple = tuple()

        def has_change_permission(self, r: HttpRequest, obj=None) -> bool:
            return False if not r.user.is_superuser else True

        def get_form(self, r: HttpRequest, obj: Any=None, **kwargs: Any) -> Any:
            if not r.user.is_superuser:
                self.exclude = self._exclude
            return super().get_form(r, obj, **kwargs)
    ```

### `#!py class CardAdmin`

Parents: `BasesWardenModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class CardAdmin(BasesWardenModelAdmin):
        list_filter = ('owner__is_active', 'card_type', 'bank', 'brand')
        search_fields = ('slug', 'card_type', 'bank', 'brand', 'owner__username')
        prepopulated_fields = {'slug': ('bank', 'name')}
        list_display = ('pk', 'slug', 'created', 'updated')
        _exclude = ('owner', 'card_type', 'number', 'expiration', 'cvv', 'brand', 'owners_name', 'note')
    ```

### `#!py class LoginCredentialAdmin`

Parents: `BasesWardenModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LoginCredentialAdmin(BasesWardenModelAdmin):
        list_filter = ('owner__is_active', 'third_party_login', 'service')
        search_fields = ('slug', 'service', 'owner__username')
        prepopulated_fields = {'slug': ('service', 'name')}
        list_display = ('pk', 'slug', 'created', 'updated')
        _exclude = ('owner', 'third_party_login', 'third_party_login_name', 'login', 'password', 'note')
    ```

### `#!py class SecurityNoteAdmin`

Parents: `BasesWardenModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class SecurityNoteAdmin(BasesWardenModelAdmin):
        list_filter = ('owner__is_active', 'note_type')
        search_fields = ('slug', 'owner__username')
        prepopulated_fields = {'slug': ('title',)}
        list_display = ('pk', 'note_type', 'slug', 'created', 'updated')
        _exclude = ('owner', 'content')
    ```



---

## Functions

### `#!py def has_change_permission`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest, obj: Unknown`

Kwargs: `#!py None`

Return Type: `#!py bool`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def has_change_permission(self, r: HttpRequest, obj=None) -> bool:
        return False if not r.user.is_superuser else True
    ```

### `#!py def get_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest, obj: Any`

Kwargs: `#!py None`

Return Type: `#!py Any`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_form(self, r: HttpRequest, obj: Any=None, **kwargs: Any) -> Any:
        if not r.user.is_superuser:
            self.exclude = self._exclude
        return super().get_form(r, obj, **kwargs)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
