from dataclasses import asdict, dataclass
from functools import lru_cache
from os import getenv, urandom
from random import seed
from typing import Any, Final

import orjson
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


COMMON_CONFIGS: dict[str, bool] = {'frozen': True, 'slots': True, 'eq': True}


@dataclass(**COMMON_CONFIGS)
class PayloadVx:
    version: int

    @property
    def as_dict(self) -> dict[str, str | int]:
        return asdict(self)


@dataclass(**COMMON_CONFIGS)
class PayloadV1(PayloadVx):
    time_cost: int
    memory_cost: int
    parallelism: int
    nonce: str
    ciphertext: str


class NoCompressHexORJSON:
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

    DISPATCH: Final[dict[int, type[PayloadVx]]] = {1: PayloadV1}

    @classmethod
    def get_payload_version(cls, payload_dict: dict[str, Any]) -> PayloadVx:
        version: int = payload_dict['version']
        payload_class: type[PayloadVx] | None = cls.DISPATCH.get(version)

        if payload_class is None:
            raise ValueError(f'Unsupported payload version: {version}')

        return payload_class(**payload_dict)

    @classmethod
    @lru_cache
    def _derive_key(cls, key1: str, key2: str, tc: int, mc: int, p: int) -> bytes:
        return hash_secret_raw(
            secret=key1.encode(),
            salt=key2.encode(),
            time_cost=tc,
            memory_cost=mc,
            parallelism=p,
            hash_len=32,
            type=Type.ID,
        )

    @classmethod
    def encrypt(
        cls,
        plaintext: str,
        key1: str,
        key2: str,
        tc: int = DEFAULT_TC,
        mc: int = DEFAULT_MC,
        p: int = DEFAULT_P,
    ) -> str:
        key: bytes = cls._derive_key(key1, key2, tc, mc, p)
        aesgcm: AESGCM = AESGCM(key)
        nonce: bytes = urandom(12)
        ciphertext: bytes = aesgcm.encrypt(nonce, plaintext.encode(), None)

        payload: PayloadV1 = PayloadV1(
            version=1,
            time_cost=tc,
            memory_cost=mc,
            parallelism=p,
            nonce=nonce.hex(),
            ciphertext=ciphertext.hex(),
        )

        return orjson.dumps(payload.as_dict).decode()

    @classmethod
    def decrypt(cls, token_b64: str, key1: str, key2: str) -> str:
        payload_dict: dict[str, Any] = orjson.loads(token_b64)

        if 'version' not in payload_dict.keys():
            raise KeyError("Payload dict couldn't perform a cast into PayloadVx.")

        payload: PayloadVx = cls.get_payload_version(payload_dict)

        if isinstance(payload, PayloadV1):
            return cls._decrypt_v1(payload, key1, key2)

        raise NotImplementedError('Payload version not implemented yet.')

    @classmethod
    def _decrypt_v1(cls, payload: PayloadV1, key1: str, key2: str) -> str:
        tc: int = payload.time_cost
        mc: int = payload.memory_cost
        p: int = payload.parallelism
        nonce: bytes = bytes.fromhex(payload.nonce)
        ciphertext: bytes = bytes.fromhex(payload.ciphertext)

        key: bytes = cls._derive_key(key1, key2, tc, mc, p)
        aesgcm: AESGCM = AESGCM(key)
        plaintext: bytes = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()
