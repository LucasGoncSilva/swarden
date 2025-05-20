
# File: `admin.py`
Path: `SWARDEN.secret`



---

## Imports

### `#!py import Any`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Any
    ```

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
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

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import Card`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import Card
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

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

??? example "SNIPPET"

    ```py
    class BasesWardenModelAdmin(ModelAdmin):
        exclude: tuple = tuple()
        _exclude: tuple = tuple()

        def has_change_permission(self, r: HttpRequest, obj=None) -> bool:
            return False if not r.user.is_superuser else True

        def get_form(self, request: HttpRequest, obj: Any=None, **kwargs: Any) -> Any:
            if not request.user.is_superuser:
                self.exclude = self._exclude
            return super().get_form(request, obj, **kwargs)
    ```

### `#!py class CardAdmin`

Parents: `BasesWardenModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class CardAdmin(BasesWardenModelAdmin):
        list_filter: Final = ('owner__is_active', 'card_type', 'bank', 'brand')
        search_fields: Final = ('card_type', 'bank', 'brand', 'owner__username', 'owner__first_name', 'owner__last_name')
        prepopulated_fields: Final = {'slug': ('bank', 'name')}
        list_display: Final = ('pk', 'slug', 'created', 'updated')
        _exclude: Final = ('owner', 'card_type', 'number', 'expiration', 'cvv', 'brand', 'owners_name', 'note')
    ```

### `#!py class LoginCredentialAdmin`

Parents: `BasesWardenModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class LoginCredentialAdmin(BasesWardenModelAdmin):
        list_filter: Final = ('owner__is_active', 'third_party_login', 'service')
        search_fields: Final = ('slug', 'serviceowner__username', 'owner__first_name', 'owner__last_name')
        prepopulated_fields: Final = {'slug': ('service', 'name')}
        list_display: Final = ('pk', 'slug', 'created', 'updated')
        _exclude: Final = ('owner', 'third_party_login', 'third_party_login_name', 'login', 'password', 'note')
    ```

### `#!py class SecurityNoteAdmin`

Parents: `BasesWardenModelAdmin`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class SecurityNoteAdmin(BasesWardenModelAdmin):
        list_filter: Final = ('owner__is_active', 'note_type')
        search_fields: Final = ('slug', 'owner__username', 'owner__first_name', 'owner__last_name')
        prepopulated_fields: Final = {'slug': ('title',)}
        list_display: Final = ('pk', 'note_type', 'slug', 'created', 'updated')
        _exclude: Final = ('owner', 'content')
    ```



---

## Functions

### `#!py def has_change_permission`

Type: `#!py ...`

Return Type: `#!py bool`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest, obj: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def has_change_permission(self, r: HttpRequest, obj=None) -> bool:
        return False if not r.user.is_superuser else True
    ```

### `#!py def get_form`

Type: `#!py ...`

Return Type: `#!py Any`

Decorators: `#!py None`

Args: `#!py self: Unknown, request: HttpRequest, obj: Any`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_form(self, request: HttpRequest, obj: Any=None, **kwargs: Any) -> Any:
        if not request.user.is_superuser:
            self.exclude = self._exclude
        return super().get_form(request, obj, **kwargs)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
