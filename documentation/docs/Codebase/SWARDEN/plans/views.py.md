# File: `views.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.plans`

No file docstring provided.

---

## Imports

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import render`

Path: `#!py django.shortcuts`

Category: trdparty

??? example "Snippet"

    ```py
    from django.shortcuts import render
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def index`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def index(r: HttpRequest) -> HttpResponse:
        free_plan: list[str] = ['Store up to 5 Credentials', 'Store up to 5 Payment Cards', 'Store up to 5 Security Notes']
        free_plan_disabled: list[str] = ['No Temporary Sharing', 'No access to Organizations', 'No local exporting']
        monthly_plan: list[str] = ['Unlimited Credentials', 'Unlimited Payment Cards', 'Unlimited Security Notes', 'Temporary Sharing', 'Access to Organizations', 'Local exporting via JSON file']
        annual_plan: list[str] = ['Everything from Monthly Plan', '16% cheaper', 'No worries for renewal soon']
        return render(r, 'plans/index.html', {'free': free_plan, 'free_disabled': free_plan_disabled, 'monthly': monthly_plan, 'annual': annual_plan})
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
