from typing import Literal

def encrypt(
    plaintext: str,
    master_key: str,
    system_pepper: str,
    policy_version_opt: Literal[1, 2, 3, 4] | None = None,
) -> str: ...
def decrypt(payload: str, master_key: str, system_pepper: str) -> str: ...
