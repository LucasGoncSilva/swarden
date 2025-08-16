# File: `utils.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN`

No file docstring provided.

---

## Imports

### `#!py import Generator`

Path: `#!py collections.abc`

Category: native

??? example "Snippet"

    ```py
    from collections.abc import Generator
    ```

### `#!py import sha256`

Path: `#!py hashlib`

Category: native

??? example "Snippet"

    ```py
    from hashlib import sha256
    ```

### `#!py import compress`

Path: `#!py itertools`

Category: native

??? example "Snippet"

    ```py
    from itertools import compress
    ```

### `#!py import product`

Path: `#!py itertools`

Category: native

??? example "Snippet"

    ```py
    from itertools import product
    ```

### `#!py import Any`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Any
    ```

### `#!py import Final`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Final
    ```

### `#!py import ActivationAccountToken`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import ActivationAccountToken
    ```

### `#!py import User`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import User
    ```

### `#!py import settings`

Path: `#!py django.conf`

Category: trdparty

??? example "Snippet"

    ```py
    from django.conf import settings
    ```

### `#!py import force_bytes`

Path: `#!py django.utils.encoding`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.encoding import force_bytes
    ```

### `#!py import urlsafe_base64_encode`

Path: `#!py django.utils.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.http import urlsafe_base64_encode
    ```



---

## Consts

### `#!py SK`

Type: `#!py Final[str]`

Value: `#!py settings.SECRET_KEY`

??? example "Snippet"

    ```py
    SK: Final[str] = settings.SECRET_KEY
    ```



---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def xor`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py token: str, key: str, encrypt: bool`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def xor(token: str, key: str, encrypt: bool=True) -> str:
        if token is None or not isinstance(token, str) or (not len(key)):
            return token
        key_repetitions: int = max(1, (len(token) + len(key) - 1) // len(key))
        expanded_key: str = (key * key_repetitions)[:len(token)]
        expanded_secret_key: str = (SK * key_repetitions)[:len(token)]
        xor_key_generator: Generator = (ord(expanded_key_char) ^ ord(secret_key_char) for expanded_key_char, secret_key_char in zip(expanded_key, expanded_secret_key))
        if encrypt:
            transformed_chars: list[str] = [chr((ord(text_char) ^ xor_key_val) + 32) for text_char, xor_key_val in zip(token, xor_key_generator)]
        else:
            transformed_chars: list[str] = [chr(ord(text_char) - 32 ^ xor_key_val) for text_char, xor_key_val in zip(token, xor_key_generator)]
        return ''.join(transformed_chars)
    ```

### `#!py def uidb64`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py uuid: str`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def uidb64(uuid: str) -> str:
        return urlsafe_base64_encode(force_bytes(uuid))
    ```

### `#!py def create_activation_account_token`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py new_user: User`

Kwargs: `#!py None`

Return Type: `#!py ActivationAccountToken`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def create_activation_account_token(new_user: User) -> ActivationAccountToken:
        token_hash: str = sha256(f'{new_user.username}{new_user.password}'.encode()).hexdigest()
        token: ActivationAccountToken = ActivationAccountToken.objects.create(value=token_hash, user=new_user, used=False)
        token.full_clean()
        return token
    ```

### `#!py def create_scenarios`

Type: `#!py generator`

Decorators: `#!py None`

Args: `#!py params: list[dict[str, Any]]`

Kwargs: `#!py None`

Return Type: `#!py Generator`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

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
