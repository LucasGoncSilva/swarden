# File: `crypt.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN`

No file docstring provided.

---

## Imports

### `#!py import b64decode`

Path: `#!py base64`

Category: native

??? example "Snippet"

    ```py
    from base64 import b64decode
    ```

### `#!py import b64encode`

Path: `#!py base64`

Category: native

??? example "Snippet"

    ```py
    from base64 import b64encode
    ```

### `#!py import dumps`

Path: `#!py json`

Category: native

??? example "Snippet"

    ```py
    from json import dumps
    ```

### `#!py import loads`

Path: `#!py json`

Category: native

??? example "Snippet"

    ```py
    from json import loads
    ```

### `#!py import getenv`

Path: `#!py os`

Category: native

??? example "Snippet"

    ```py
    from os import getenv
    ```

### `#!py import urandom`

Path: `#!py os`

Category: native

??? example "Snippet"

    ```py
    from os import urandom
    ```

### `#!py import TypedDict`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import TypedDict
    ```

### `#!py import compress`

Path: `#!py zlib`

Category: native

??? example "Snippet"

    ```py
    from zlib import compress
    ```

### `#!py import decompress`

Path: `#!py zlib`

Category: native

??? example "Snippet"

    ```py
    from zlib import decompress
    ```

### `#!py import Type`

Path: `#!py argon2.low_level`

Category: trdparty

??? example "Snippet"

    ```py
    from argon2.low_level import Type
    ```

### `#!py import hash_secret_raw`

Path: `#!py argon2.low_level`

Category: trdparty

??? example "Snippet"

    ```py
    from argon2.low_level import hash_secret_raw
    ```

### `#!py import AESGCM`

Path: `#!py cryptography.hazmat.primitives.ciphers.aead`

Category: trdparty

??? example "Snippet"

    ```py
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    ```



---

## Consts

### `#!py DEFAULT_TC`

Type: `#!py int`

Value: `#!py `

??? example "Snippet"

    ```py
    DEFAULT_TC: int
    ```

### `#!py DEFAULT_MC`

Type: `#!py int`

Value: `#!py `

??? example "Snippet"

    ```py
    DEFAULT_MC: int
    ```

### `#!py DEFAULT_P`

Type: `#!py int`

Value: `#!py `

??? example "Snippet"

    ```py
    DEFAULT_P: int
    ```

### `#!py _DEFAULT_VALUES`

Type: `#!py str | None`

Value: `#!py getenv('DEFAULT_TC_MC_P', '3,65536,1')`

??? example "Snippet"

    ```py
    _DEFAULT_VALUES: str | None = getenv('DEFAULT_TC_MC_P', '3,65536,1')
    ```

### `#!py (DEFAULT_TC, DEFAULT_MC, DEFAULT_P)`

Type: `#!py Unknown`

Value: `#!py map(int, _DEFAULT_VALUES.split(','))`

??? example "Snippet"

    ```py
    DEFAULT_TC, DEFAULT_MC, DEFAULT_P = map(int, _DEFAULT_VALUES.split(','))
    ```

### `#!py (DEFAULT_TC, DEFAULT_MC, DEFAULT_P)`

Type: `#!py Unknown`

Value: `#!py (3, 65536, 1)`

??? example "Snippet"

    ```py
    DEFAULT_TC, DEFAULT_MC, DEFAULT_P = (3, 65536, 1)
    ```



---

## Classes

### `#!py class PayloadV1`

Parents: `TypedDict`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class PayloadV1(TypedDict):
        version: int
        time_cost: int
        memory_cost: int
        parallelism: int
        nonce: str
        ciphertext: str
    ```

### `#!py class sWardenCryptography`

Parents: `None`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class sWardenCryptography:
        DEFAULT_TC: int
        DEFAULT_MC: int
        DEFAULT_P: int
        _DEFAULT_VALUES: str | None = getenv('DEFAULT_TC_MC_P', '3,65536,1')
        try:
            DEFAULT_TC, DEFAULT_MC, DEFAULT_P = map(int, _DEFAULT_VALUES.split(','))
        except ValueError:
            DEFAULT_TC, DEFAULT_MC, DEFAULT_P = (3, 65536, 1)

        @classmethod
        def _derive_key(cls, key1: str, key2: str, tc: int, mc: int, p: int) -> bytes:
            return hash_secret_raw(secret=key1.encode(), salt=key2.encode(), time_cost=tc, memory_cost=mc, parallelism=p, hash_len=32, type=Type.ID)

        @classmethod
        def encrypt(cls, plaintext: str, key1: str, key2: str, tc: int=DEFAULT_TC, mc: int=DEFAULT_MC, p: int=DEFAULT_P) -> str:
            compressed_data = compress(plaintext.encode())
            key = cls._derive_key(key1, key2, tc, mc, p)
            aesgcm = AESGCM(key)
            nonce = urandom(12)
            ciphertext = aesgcm.encrypt(nonce, compressed_data, None)
            payload: PayloadV1 = {'version': 1, 'time_cost': tc, 'memory_cost': mc, 'parallelism': p, 'nonce': b64encode(nonce).decode(), 'ciphertext': b64encode(ciphertext).decode()}
            return b64encode(dumps(payload).encode()).decode()

        @classmethod
        def decrypt(cls, token_b64: str, key1: str, key2: str) -> str:
            try:
                decoded = b64decode(token_b64)
                payload: PayloadV1 = loads(decoded.decode())
            except Exception as e:
                raise ValueError(f'Token inválido ou malformado: {e}')
            if payload.get('version') == 1:
                return cls._decrypt_v1(payload, key1, key2)
            else:
                raise ValueError(f'Versão de payload não suportada: {payload.get('v')}')

        @classmethod
        def _decrypt_v1(cls, payload: PayloadV1, key1: str, key2: str) -> str:
            for key in ('time_cost', 'memory_cost', 'parallelism', 'nonce', 'ciphertext'):
                if key not in payload:
                    raise ValueError(f"Campo obrigatório ausente no payload: '{key}'")
            tc = int(payload['time_cost'])
            mc = int(payload['memory_cost'])
            p = int(payload['parallelism'])
            nonce = b64decode(str(payload['nonce']))
            ciphertext = b64decode(str(payload['ciphertext']))
            key = cls._derive_key(key1, key2, tc, mc, p)
            aesgcm = AESGCM(key)
            try:
                plaintext = aesgcm.decrypt(nonce, ciphertext, None)
                decompressed_data = decompress(plaintext)
                return decompressed_data.decode()
            except Exception as e:
                raise ValueError(f'Falha ao descriptografar: {e}')
    ```



---

## Functions

### `#!py def _derive_key`

Type: `#!py method`

Decorators: `#!py classmethod`

Args: `#!py cls: Unknown, key1: str, key2: str, tc: int, mc: int, p: int`

Kwargs: `#!py None`

Return Type: `#!py bytes`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @classmethod
    def _derive_key(cls, key1: str, key2: str, tc: int, mc: int, p: int) -> bytes:
        return hash_secret_raw(secret=key1.encode(), salt=key2.encode(), time_cost=tc, memory_cost=mc, parallelism=p, hash_len=32, type=Type.ID)
    ```

### `#!py def encrypt`

Type: `#!py method`

Decorators: `#!py classmethod`

Args: `#!py cls: Unknown, plaintext: str, key1: str, key2: str, tc: int, mc: int, p: int`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @classmethod
    def encrypt(cls, plaintext: str, key1: str, key2: str, tc: int=DEFAULT_TC, mc: int=DEFAULT_MC, p: int=DEFAULT_P) -> str:
        compressed_data = compress(plaintext.encode())
        key = cls._derive_key(key1, key2, tc, mc, p)
        aesgcm = AESGCM(key)
        nonce = urandom(12)
        ciphertext = aesgcm.encrypt(nonce, compressed_data, None)
        payload: PayloadV1 = {'version': 1, 'time_cost': tc, 'memory_cost': mc, 'parallelism': p, 'nonce': b64encode(nonce).decode(), 'ciphertext': b64encode(ciphertext).decode()}
        return b64encode(dumps(payload).encode()).decode()
    ```

### `#!py def decrypt`

Type: `#!py method`

Decorators: `#!py classmethod`

Args: `#!py cls: Unknown, token_b64: str, key1: str, key2: str`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @classmethod
    def decrypt(cls, token_b64: str, key1: str, key2: str) -> str:
        try:
            decoded = b64decode(token_b64)
            payload: PayloadV1 = loads(decoded.decode())
        except Exception as e:
            raise ValueError(f'Token inválido ou malformado: {e}')
        if payload.get('version') == 1:
            return cls._decrypt_v1(payload, key1, key2)
        else:
            raise ValueError(f'Versão de payload não suportada: {payload.get('v')}')
    ```

### `#!py def _decrypt_v1`

Type: `#!py method`

Decorators: `#!py classmethod`

Args: `#!py cls: Unknown, payload: PayloadV1, key1: str, key2: str`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @classmethod
    def _decrypt_v1(cls, payload: PayloadV1, key1: str, key2: str) -> str:
        for key in ('time_cost', 'memory_cost', 'parallelism', 'nonce', 'ciphertext'):
            if key not in payload:
                raise ValueError(f"Campo obrigatório ausente no payload: '{key}'")
        tc = int(payload['time_cost'])
        mc = int(payload['memory_cost'])
        p = int(payload['parallelism'])
        nonce = b64decode(str(payload['nonce']))
        ciphertext = b64decode(str(payload['ciphertext']))
        key = cls._derive_key(key1, key2, tc, mc, p)
        aesgcm = AESGCM(key)
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            decompressed_data = decompress(plaintext)
            return decompressed_data.decode()
        except Exception as e:
            raise ValueError(f'Falha ao descriptografar: {e}')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
