
# File: `widgets.py`
Path: `SWARDEN.secret.month`



---

## Imports

### `#!py import date`

Path: `#!py datetime`

Category: Native

??? example "SNIPPET"

    ```py
    from datetime import date
    ```

### `#!py import widgets`

Path: `#!py django.forms`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.forms import widgets
    ```

### `#!py import static`

Path: `#!py django.templatetags.static`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.templatetags.static import static
    ```

### `#!py import MONTHS`

Path: `#!py django.utils.dates`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.utils.dates import MONTHS
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

### `#!py D`

Type: `#!py Unknown`

Value: `#!py date(day=1, month=int(datelist[0]), year=int(datelist[1]))`

??? example "SNIPPET"

    ```py
    D = date(day=1, month=int(datelist[0]), year=int(datelist[1]))
    ```



---

## Classes

### `#!py class MonthSelectorWidget`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class MonthSelectorWidget(widgets.MultiWidget):

        def __init__(self, attrs=None):
            _attrs = attrs or {}
            _attrs['class'] = (_attrs.get('class', '') + ' w-month-year').strip()
            _widgets = [widgets.Select(attrs=_attrs, choices=MONTHS.items())]
            _attrs['class'] += ' w-year'
            _widgets.append(widgets.NumberInput(attrs=_attrs))
            super(MonthSelectorWidget, self).__init__(_widgets, attrs)

        @property
        def media(self):
            media = self._get_media()
            media.add_css({'screen': (static('month/field/widget_month.css'),)})
            return media

        def decompress(self, value):
            if value:
                if isinstance(value, string_type):
                    m = int(value[5:7])
                    y = int(value[:4])
                    return [m, y]
                return [value.month, value.year]
            return [None, None]

        def format_output(self, rendered_widgets):
            return ''.join(rendered_widgets)

        def value_from_datadict(self, data, files, name):
            datelist = [widget.value_from_datadict(data, files, name + '_%s' % i) for (i, widget) in enumerate(self.widgets)]
            try:
                D = date(day=1, month=int(datelist[0]), year=int(datelist[1]))
            except ValueError:
                return ''
            else:
                return str(D)
    ```



---

## Functions

### `#!py def __init__`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, attrs: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def __init__(self, attrs=None):
        _attrs = attrs or {}
        _attrs['class'] = (_attrs.get('class', '') + ' w-month-year').strip()
        _widgets = [widgets.Select(attrs=_attrs, choices=MONTHS.items())]
        _attrs['class'] += ' w-year'
        _widgets.append(widgets.NumberInput(attrs=_attrs))
        super(MonthSelectorWidget, self).__init__(_widgets, attrs)
    ```

### `#!py def media`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py property`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @property
    def media(self):
        media = self._get_media()
        media.add_css({'screen': (static('month/field/widget_month.css'),)})
        return media
    ```

### `#!py def decompress`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, value: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def decompress(self, value):
        if value:
            if isinstance(value, string_type):
                m = int(value[5:7])
                y = int(value[:4])
                return [m, y]
            return [value.month, value.year]
        return [None, None]
    ```

### `#!py def format_output`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, rendered_widgets: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)
    ```

### `#!py def value_from_datadict`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown, data: Unknown, files: Unknown, name: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def value_from_datadict(self, data, files, name):
        datelist = [widget.value_from_datadict(data, files, name + '_%s' % i) for (i, widget) in enumerate(self.widgets)]
        try:
            D = date(day=1, month=int(datelist[0]), year=int(datelist[1]))
        except ValueError:
            return ''
        else:
            return str(D)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
