
# File: `models.py`
Path: `SWARDEN.secret.month`



---

## Imports

### `#!py import datetime`

Path: `#!py None`

Category: Native

??? example "SNIPPET"

    ```py
    import datetime
    ```

### `#!py import exceptions`

Path: `#!py django.core`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core import exceptions
    ```

### `#!py import models`

Path: `#!py django.db`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db import models
    ```

### `#!py import gettext_lazy`

Path: `#!py django.utils.translation`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.utils.translation import gettext_lazy
    ```

### `#!py import Month`

Path: `#!py None`

Category: Local

??? example "SNIPPET"

    ```py
    from None import Month
    ```

### `#!py import forms`

Path: `#!py None`

Category: Local

??? example "SNIPPET"

    ```py
    from None import forms
    ```

### `#!py import widgets`

Path: `#!py None`

Category: Local

??? example "SNIPPET"

    ```py
    from None import widgets
    ```

### `#!py import string_type`

Path: `#!py util`

Category: Local

??? example "SNIPPET"

    ```py
    from util import string_type
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

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

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

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_prep_value(self, value):
        month = self.to_python(value)
        if month is not None:
            return month.first_day()
        return None
    ```

### `#!py def from_db_value`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown, expression: Unknown, connection: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def from_db_value(self, value, expression, connection):
        return self.to_python(value)
    ```

### `#!py def clean`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown, instance: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def clean(self, value, instance):
        return self.to_python(value)
    ```

### `#!py def formfield`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

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
