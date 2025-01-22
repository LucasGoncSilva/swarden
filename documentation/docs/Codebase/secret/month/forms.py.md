
# File: `forms.py`
Path: `SWARDEN.secret.month`



---

## Imports

### `#!py import forms`

Path: `#!py django`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django import forms
    ```

### `#!py import MonthSelectorWidget`

Path: `#!py widgets`

Category: Local

??? example "SNIPPET"

    ```py
    from widgets import MonthSelectorWidget
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class MonthField`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class MonthField(forms.DateField):
        widget = MonthSelectorWidget
    ```



---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
