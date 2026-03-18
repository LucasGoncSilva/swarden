from os import getenv
from random import seed
from typing import Any

import rust


COMMON_CONFIGS: dict[str, bool] = {'frozen': True, 'slots': True, 'eq': True}


class RustAlgo:
    if (seed_value := getenv('CRYPTOSEED')) is None:
        raise ValueError('CRYPTOSEED cannot be None!')  # pragma: no cover

    seed(seed_value)

    DEFAULT_TC: int
    DEFAULT_MC: int
    DEFAULT_P: int
    _DEFAULT_VALUES: str = getenv('DEFAULT_TC_MC_P', '6,131072,1')

    try:
        DEFAULT_TC, DEFAULT_MC, DEFAULT_P = map(int, _DEFAULT_VALUES.split(','))
    except ValueError:  # pragma: no cover
        DEFAULT_TC, DEFAULT_MC, DEFAULT_P = 6, 131072, 1

    @classmethod
    def encrypt(
        cls,
        plaintext: str,
        key1: str,
        key2: str,
        *args: Any,
    ) -> str:
        return rust.encrypt(plaintext, key1, key2, 0)

    @classmethod
    def decrypt(cls, payload: str, key1: str, key2: str) -> str:
        return rust.decrypt(payload, key1, key2)
