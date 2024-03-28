from typing import Any, Generator

from django.http import HttpRequest
from django.conf import settings


SK: str = settings.SECRET_KEY


def get_ip_address(r: HttpRequest) -> Any | None:
    x_forwarded_for = r.META.get('HTTP_X_FORWARDED_FOR')
    ip: Any | None = (
        x_forwarded_for.split(',')[0] if x_forwarded_for else r.META.get('REMOTE_ADDR')
    )

    return ip


def xor(text: str, key: str, encrypt: bool = True) -> str:
    if text is None or not len(key):
        return text

    # Calculate the necessary key repetitions
    key_repetitions = max(1, (len(text) + len(key) - 1) // len(key))

    # Expand the key and secret key to match the text length
    expanded_key = (key * key_repetitions)[: len(text)]
    expanded_secret_key = (SK * key_repetitions)[: len(text)]

    # Create a generator for XORed values
    xor_key_generator: Generator = (
        ord(expanded_key_char) ^ ord(secret_key_char)
        for expanded_key_char, secret_key_char in zip(expanded_key, expanded_secret_key)
    )

    # Encrypt or decrypt the text
    if encrypt:
        transformed_chars = [
            chr((ord(text_char) ^ xor_key_val) + 32)
            for text_char, xor_key_val in zip(text, xor_key_generator)
        ]
    else:
        transformed_chars = [
            chr((ord(text_char) - 32) ^ xor_key_val)
            for text_char, xor_key_val in zip(text, xor_key_generator)
        ]

    return ''.join(transformed_chars)
