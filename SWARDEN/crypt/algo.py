from typing import Literal

import rust


class sWardenCryptography:
    @classmethod
    def encrypt(
        cls,
        plaintext: str,
        master_key: str,
        system_pepper: str,
        policy_version_opt: Literal[1, 2, 3, 4] | None = None,
    ) -> str:
        return rust.encrypt(plaintext, master_key, system_pepper, policy_version_opt)

    @classmethod
    def decrypt(cls, payload: str, master_key: str, system_pepper: str) -> str:
        return rust.decrypt(payload, master_key, system_pepper)
