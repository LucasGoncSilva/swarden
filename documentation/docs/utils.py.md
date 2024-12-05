
# File: `utils.py`
Path: `SWARDEN`



---

## Imports

### `#!py import sha256`

Path: `#!py hashlib`

Category: Native

??? example "SNIPPET"

    ```py
    from hashlib import sha256
    ```

### `#!py import StringIO`

Path: `#!py io`

Category: Native

??? example "SNIPPET"

    ```py
    from io import StringIO
    ```

### `#!py import compress`

Path: `#!py itertools`

Category: Native

??? example "SNIPPET"

    ```py
    from itertools import compress
    ```

### `#!py import product`

Path: `#!py itertools`

Category: Native

??? example "SNIPPET"

    ```py
    from itertools import product
    ```

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

### `#!py import Generator`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Generator
    ```

### `#!py import Literal`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Literal
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

### `#!py import settings`

Path: `#!py django.conf`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.conf import settings
    ```

### `#!py import EmailMessage`

Path: `#!py django.core.mail`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.mail import EmailMessage
    ```

### `#!py import validate_email`

Path: `#!py django.core.validators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.validators import validate_email
    ```

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import force_bytes`

Path: `#!py django.utils.encoding`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.utils.encoding import force_bytes
    ```

### `#!py import urlsafe_base64_encode`

Path: `#!py django.utils.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.utils.http import urlsafe_base64_encode
    ```



---

## Consts

### `#!py SK`

Type: `#!py str`

Value: `#!py settings.SECRET_KEY`

??? example "SNIPPET"

    ```py
    SK: str = settings.SECRET_KEY
    ```

### `#!py NO_DATA_TO_EXPORT`

Type: `#!py Final[str]`

Value: `#!py 'Não há dados para exportação.'`

??? example "SNIPPET"

    ```py
    NO_DATA_TO_EXPORT: Final[str] = 'Não há dados para exportação.'
    ```

### `#!py SUCCESS_DATA_EXPORTING`

Type: `#!py Final[str]`

Value: `#!py 'Dados exportados com sucesso.'`

??? example "SNIPPET"

    ```py
    SUCCESS_DATA_EXPORTING: Final[str] = 'Dados exportados com sucesso.'
    ```

### `#!py ACTIVATE_ACCOUNT_TOKEN_SEND`

Type: `#!py Final[str]`

Value: `#!py 'Sua conta foi criada com sucesso, contudo, você deve ativá-la. Para fazer isso, clique no link abaixo:\n\n\n{domain}/conta/ativar/{uidb64}/{token}\n\nEquipe sWarden'`

??? example "SNIPPET"

    ```py
    ACTIVATE_ACCOUNT_TOKEN_SEND: Final[str] = 'Sua conta foi criada com sucesso, contudo, você deve ativá-la. Para fazer isso, clique no link abaixo:\n\n\n{domain}/conta/ativar/{uidb64}/{token}\n\nEquipe sWarden'
    ```

### `#!py ACTIVATE_ACCOUNT_CONFIRM_DONE`

Type: `#!py Final[str]`

Value: `#!py 'A partir de agora a sua conta está ativa e você pode utilizar dos recursos do sistema para armazenar seus dados sensíveis.\n\nEquipe sWarden'`

??? example "SNIPPET"

    ```py
    ACTIVATE_ACCOUNT_CONFIRM_DONE: Final[str] = 'A partir de agora a sua conta está ativa e você pode utilizar dos recursos do sistema para armazenar seus dados sensíveis.\n\nEquipe sWarden'
    ```



---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def get_ip_address`

Type: `#!py ...`

Return Type: `#!py Any | None`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_ip_address(r: HttpRequest) -> Any | None:
        x_forwarded_for: Any | None = r.META.get('HTTP_X_FORWARDED_FOR')
        ip: Any | None = x_forwarded_for.split(',')[0] if x_forwarded_for else r.META.get('REMOTE_ADDR')
        return ip
    ```

### `#!py def xor`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py text: str, key: str, encrypt: bool`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def xor(text: str, key: str, encrypt: bool=True) -> str:
        if text is None or not isinstance(text, str) or (not len(key)):
            return text
        key_repetitions: int = max(1, (len(text) + len(key) - 1) // len(key))
        expanded_key: str = (key * key_repetitions)[:len(text)]
        expanded_secret_key: str = (SK * key_repetitions)[:len(text)]
        xor_key_generator: Generator = (ord(expanded_key_char) ^ ord(secret_key_char) for (expanded_key_char, secret_key_char) in zip(expanded_key, expanded_secret_key))
        if encrypt:
            transformed_chars: list[str] = [chr((ord(text_char) ^ xor_key_val) + 32) for (text_char, xor_key_val) in zip(text, xor_key_generator)]
        else:
            transformed_chars: list[str] = [chr(ord(text_char) - 32 ^ xor_key_val) for (text_char, xor_key_val) in zip(text, xor_key_generator)]
        return ''.join(transformed_chars)
    ```

### `#!py def send_email_activation_account_token`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py domain: str, new_user: User, password: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def send_email_activation_account_token(domain: str, new_user: User, password: str) -> None:
        if not isinstance(domain, str) or not isinstance(new_user, User) or (not isinstance(password, str)):
            raise TypeError(f'{domain}, {new_user} and {password} are invalid arguments')
        validate_email(new_user.email)
        token_hash: str = sha256(f'{new_user.username}{password}'.encode()).hexdigest()
        uidb64: str = urlsafe_base64_encode(force_bytes(new_user.pk))
        token: ActivationAccountToken = ActivationAccountToken.objects.create(value=token_hash, user=new_user, used=False)
        token.full_clean()
        email: EmailMessage = EmailMessage(subject='Ativação de Conta | sWarden', body=ACTIVATE_ACCOUNT_TOKEN_SEND.format(domain=domain, uidb64=uidb64, token=token_hash), from_email=settings.EMAIL_HOST_USER, to=[str(new_user.email)])
        email.send()
    ```

### `#!py def send_email_activate_account_completed`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py user_email: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def send_email_activate_account_completed(user_email: str) -> None:
        validate_email(user_email)
        email: EmailMessage = EmailMessage(subject='Ativação de Conta | sWarden', body=ACTIVATE_ACCOUNT_CONFIRM_DONE, from_email=settings.EMAIL_HOST_USER, to=[user_email])
        email.send()
    ```

### `#!py def send_email_exporting_secrets`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py secret_type: Literal['Credenciais', 'Cartões', 'Anotações'], csvfile: StringIO, user_email: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def send_email_exporting_secrets(secret_type: Literal['Credenciais', 'Cartões', 'Anotações'], csvfile: StringIO, user_email: str) -> None:
        validate_email(user_email)
        content: str = f'Aqui estão seus segredos armazenados em "{secret_type}" no sWarden.\n\nEquipe sWarden'
        email: EmailMessage = EmailMessage(subject='Exportação de Segredos | sWarden', body=content, from_email=settings.EMAIL_HOST_USER, to=[user_email])
        email.attach('anotacoes.csv', csvfile.getvalue(), 'text/csv')
        email.send()
    ```

### `#!py def create_scenarios`

Type: `#!py ...`

Return Type: `#!py Generator`

Decorators: `#!py None`

Args: `#!py params: list[dict[str, Any]]`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def create_scenarios(params: list[dict[str, Any]]) -> Generator:
        for case in product([0, 1], repeat=len(params)):
            if all(case):
                break
            _temp: compress[dict[str, Any]] = compress(params, case)
            temp: list[dict[str, Any]] = list(_temp)
            scenario: dict = {}
            for param in temp:
                scenario.update(param)
            yield (case, scenario)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
