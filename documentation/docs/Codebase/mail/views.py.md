
# File: `views.py`
Path: `SWARDEN.mail`



---

## Imports

### `#!py import writer`

Path: `#!py csv`

Category: Native

??? example "SNIPPET"

    ```py
    from csv import writer
    ```

### `#!py import StringIO`

Path: `#!py io`

Category: Native

??? example "SNIPPET"

    ```py
    from io import StringIO
    ```

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import Literal`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Literal
    ```

### `#!py import Type`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Type
    ```

### `#!py import login_required`

Path: `#!py django.contrib.auth.decorators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth.decorators import login_required
    ```

### `#!py import error`

Path: `#!py django.contrib.messages`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.messages import error
    ```

### `#!py import success`

Path: `#!py django.contrib.messages`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.messages import success
    ```

### `#!py import warning`

Path: `#!py django.contrib.messages`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.messages import warning
    ```

### `#!py import QuerySet`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import QuerySet
    ```

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import HttpResponseRedirect`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpResponseRedirect
    ```

### `#!py import reverse`

Path: `#!py django.urls`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.urls import reverse
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

### `#!py import NO_DATA_TO_EXPORT`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import NO_DATA_TO_EXPORT
    ```

### `#!py import SUCCESS_DATA_EXPORTING`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import SUCCESS_DATA_EXPORTING
    ```

### `#!py import send_email_exporting_secrets`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import send_email_exporting_secrets
    ```

### `#!py import WakeDatabase`

Path: `#!py mail.models`

Category: Local

??? example "SNIPPET"

    ```py
    from mail.models import WakeDatabase
    ```



---

## Consts

### `#!py CREDENTIALS`

Type: `#!py Final[str]`

Value: `#!py 'Credenciais'`

??? example "SNIPPET"

    ```py
    CREDENTIALS: Final[str] = 'Credenciais'
    ```

### `#!py CARDS`

Type: `#!py Final[str]`

Value: `#!py 'Cartões'`

??? example "SNIPPET"

    ```py
    CARDS: Final[str] = 'Cartões'
    ```

### `#!py SECURITY_NOTES`

Type: `#!py Final[str]`

Value: `#!py 'Anotações'`

??? example "SNIPPET"

    ```py
    SECURITY_NOTES: Final[str] = 'Anotações'
    ```



---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def export_secrets_no_argument`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py login_required(login_url='/conta/entrar')`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_required(login_url='/conta/entrar')
    def export_secrets_no_argument(r: HttpRequest):
        return HttpResponseRedirect(reverse('home:index'))
    ```

### `#!py def export_secrets`

Type: `#!py ...`

Return Type: `#!py HttpResponseRedirect`

Decorators: `#!py login_required(login_url='/conta/entrar')`

Args: `#!py r: HttpRequest, secret_type: Literal['Credenciais', 'Cartões', 'Anotações']`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_required(login_url='/conta/entrar')
    def export_secrets(r: HttpRequest, secret_type: Literal['Credenciais', 'Cartões', 'Anotações']) -> HttpResponseRedirect:
        CREDENTIALS: Final[str] = 'Credenciais'
        CARDS: Final[str] = 'Cartões'
        SECURITY_NOTES: Final[str] = 'Anotações'
        if secret_type not in [CREDENTIALS, CARDS, SECURITY_NOTES]:
            warning(r, 'Impossível exportar segredos do tipo informado.')
            return HttpResponseRedirect(reverse('home:index'))
        dispatch_models: dict[str, Type[LoginCredential] | Type[Card] | Type[SecurityNote]] = {CREDENTIALS: LoginCredential, CARDS: Card, SECURITY_NOTES: SecurityNote}
        query: QuerySet = dispatch_models[secret_type].objects.filter(owner=r.user)
        dispatch_redirect: dict[str, str] = {CREDENTIALS: 'secret:credential_list_view', CARDS: 'secret:card_list_view', SECURITY_NOTES: 'secret:note_list_view'}
        if not query.exists():
            error(r, NO_DATA_TO_EXPORT)
            return HttpResponseRedirect(reverse(dispatch_redirect[secret_type]))
        csvfile: StringIO = StringIO()
        csvwriter = writer(csvfile, delimiter='¬', doublequote=True)
        if secret_type == CREDENTIALS:
            csvwriter.writerow(['Serviço', 'Apelido', 'Login 3rd', 'Apelido Login 3rd', 'Login', 'Senha'])
            for i in query:
                csvwriter.writerow([i.get_service_display(), i.name, i.thirdy_party_login, i.thirdy_party_login_name, i.login, i.password])
        elif secret_type == CARDS:
            csvwriter.writerow(['Apelido', 'Tipo', 'Número', 'Expiração', 'CVV', 'Banco', 'Bandeira', 'Titular'])
            for i in query:
                csvwriter.writerow([i.name, i.get_card_type_display(), i.number, i.expiration, i.cvv, i.get_bank_display(), i.get_brand_display(), i.owners_name])
        elif secret_type == SECURITY_NOTES:
            csvwriter.writerow(['Título', 'Conteúdo'])
            for i in query:
                csvwriter.writerow([i.title, i.content])
        send_email_exporting_secrets(secret_type, csvfile, str(r.user.email))
        success(r, SUCCESS_DATA_EXPORTING)
        return HttpResponseRedirect(reverse(dispatch_redirect[secret_type]))
    ```

### `#!py def wake_db`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def wake_db(r: HttpRequest) -> HttpResponse:
        WakeDatabase.objects.create()
        e = WakeDatabase.objects.all()
        if e.count() > 3:
            e.delete()
        return HttpResponse(e.count())
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
