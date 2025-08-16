# File: `models.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.secret.month`

No file docstring provided.

---

## Imports

### `#!py import datetime`

Path: `#!py None`

Category: native

??? example "Snippet"

    ```py
    import datetime
    ```

### `#!py import exceptions`

Path: `#!py django.core`

Category: trdparty

??? example "Snippet"

    ```py
    from django.core import exceptions
    ```

### `#!py import models`

Path: `#!py django.db`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db import models
    ```

### `#!py import gettext_lazy`

Path: `#!py django.utils.translation`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.translation import gettext_lazy
    ```

### `#!py import Month`

Path: `#!py None`

Category: trdparty

??? example "Snippet"

    ```py
    from None import Month
    ```

### `#!py import forms`

Path: `#!py None`

Category: trdparty

??? example "Snippet"

    ```py
    from None import forms
    ```

### `#!py import widgets`

Path: `#!py None`

Category: trdparty

??? example "Snippet"

    ```py
    from None import widgets
    ```

### `#!py import string_type`

Path: `#!py util`

Category: trdparty

??? example "Snippet"

    ```py
    from util import string_type
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class MonthField`

Parents: `None`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class MonthField(models.DateField):
        description = 'A specific month of a specific year.'
        widget = widgets.MonthSelectorWidget
        default_error_messages = {'invalid_year': _('Year informed invalid. Enter at least 4 digits.')}

        def to_python(self, value):
            if isinstance(value, Month):
                month = value
            elif isinstance(value, datetime.date):
                month = Month.from_date(value)
                if len(str(month.year)) < 4:
                    raise exceptions.ValidationError(self.error_messages['invalid_year'], code='invalid_year', params={'value': value})
            elif isinstance(value, string_type):
                month = Month.from_string(value)
            else:
                month = None
            return month

        def get_prep_value(self, value):
            month = self.to_python(value)
            if month is not None:
                return month.first_day()
            return None

        def from_db_value(self, value, expression, connection):
            return self.to_python(value)

        def clean(self, value, instance):
            return self.to_python(value)

        def formfield(self, **kwargs):
            kwargs['widget'] = self.widget
            defaults = {'form_class': forms.MonthField}
            defaults.update(kwargs)
            return super(MonthField, self).formfield(**defaults)
    ```



---

## Functions

### `#!py def to_python`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def to_python(self, value):
        if isinstance(value, Month):
            month = value
        elif isinstance(value, datetime.date):
            month = Month.from_date(value)
            if len(str(month.year)) < 4:
                raise exceptions.ValidationError(self.error_messages['invalid_year'], code='invalid_year', params={'value': value})
        elif isinstance(value, string_type):
            month = Month.from_string(value)
        else:
            month = None
        return month
    ```

### `#!py def get_prep_value`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_prep_value(self, value):
        month = self.to_python(value)
        if month is not None:
            return month.first_day()
        return None
    ```

### `#!py def from_db_value`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown, expression: Unknown, connection: Unknown`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def from_db_value(self, value, expression, connection):
        return self.to_python(value)
    ```

### `#!py def clean`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown, instance: Unknown`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def clean(self, value, instance):
        return self.to_python(value)
    ```

### `#!py def formfield`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def formfield(self, **kwargs):
        kwargs['widget'] = self.widget
        defaults = {'form_class': forms.MonthField}
        defaults.update(kwargs)
        return super(MonthField, self).formfield(**defaults)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
