
# File: `forms.py`
Path: `SWARDEN.account`



---

## Imports

### `#!py import forms`

Path: `#!py django.contrib.auth`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth import forms
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

### `#!py class UserChangeForm`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class UserChangeForm(forms.UserChangeForm):

        class Meta(forms.UserChangeForm.Meta):
            model = User
    ```

### `#!py class UserCreationForm`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class UserCreationForm(forms.UserCreationForm):

        class Meta(forms.UserCreationForm.Meta):
            model = User
    ```

### `#!py class Meta`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Meta(forms.UserChangeForm.Meta):
        model = User
    ```

### `#!py class Meta`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Meta(forms.UserCreationForm.Meta):
        model = User
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
