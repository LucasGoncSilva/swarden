from base64 import b64decode, b64encode
from json import dumps, loads
from os import getenv, urandom
from typing import TypedDict
from zlib import compress, decompress

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class PayloadV1(TypedDict):
    version: int
    time_cost: int
    memory_cost: int
    parallelism: int
    nonce: str
    ciphertext: str


class sWardenCryptography:
    DEFAULT_TC: int
    DEFAULT_MC: int
    DEFAULT_P: int
    _DEFAULT_VALUES: str | None = getenv('DEFAULT_TC_MC_P', '3,65536,1')

    try:
        DEFAULT_TC, DEFAULT_MC, DEFAULT_P = map(int, _DEFAULT_VALUES.split(','))
    except ValueError:
        DEFAULT_TC, DEFAULT_MC, DEFAULT_P = 3, 65536, 1

    @classmethod
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
        compressed_data = compress(plaintext.encode())

        key = cls._derive_key(key1, key2, tc, mc, p)
        aesgcm = AESGCM(key)
        nonce = urandom(12)
        ciphertext = aesgcm.encrypt(nonce, compressed_data, None)

        payload: PayloadV1 = {
            'version': 1,
            'time_cost': tc,
            'memory_cost': mc,
            'parallelism': p,
            'nonce': b64encode(nonce).decode(),
            'ciphertext': b64encode(ciphertext).decode(),
        }

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
            raise ValueError(f'Versão de payload não suportada: {payload.get("v")}')

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
