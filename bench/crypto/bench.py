# ruff: noqa: E402 E501

import statistics
import timeit
from os import environ
from typing import Protocol, cast

from pympler import asizeof
from tabulate import tabulate


environ['CRYPTOSEED'] = 'justsomeletters'


# Configs
REPETICOES = 10
EXECUCOES_POR_CICLO = 100_000
WARMUP_RUNS = 1_000

# Testing Data
KEY1: str = 'master-key-super-secret' * 2
KEY2: str = 'salt-random-string' * 2
PLAINTEXT: str = 'Este é um teste de performance padrão'


from default_algo import Default
from no_compress_hex_orjson import NoCompressHexORJSON
from no_compress_orjson_algo import NoCompressORJSON
from orjson_algo import ORJSON
from rust_algo import RustAlgo
from typeddict_orjson_algo import TypedDictORJSON


class EncryptingClasseProtocol(Protocol):
    @classmethod
    def encrypt(
        cls,
        plaintext: str,
        key1: str,
        key2: str,
        tc: int = 6,
        mc: int = 131072,
        p: int = 1,
    ) -> str: ...

    @classmethod
    def decrypt(cls, token_b64: str, key1: str, key2: str) -> str: ...


def come_and_go(cls: EncryptingClasseProtocol) -> str:
    return cls.decrypt(cls.encrypt(PLAINTEXT, KEY1, KEY2), KEY1, KEY2)


def run_benchmark() -> None:
    classes: list[tuple[str, EncryptingClasseProtocol]] = [
        ('Standard', Default),
        ('ORJSON', ORJSON),
        ('TD + ORJSON', TypedDictORJSON),
        ('no compress + OJSON', NoCompressORJSON),
        ('no compress + HEX + OJSON', NoCompressHexORJSON),
        ('Rust', cast(EncryptingClasseProtocol, RustAlgo)),
    ]

    results: list[list[str | float]] = []
    default_bytesize: int = classes[0][1].encrypt(PLAINTEXT, KEY1, KEY2)

    assert (
        come_and_go(classes[0][1])
        == come_and_go(classes[1][1])
        == come_and_go(classes[2][1])
        == come_and_go(classes[3][1])
        == come_and_go(classes[4][1])
        == come_and_go(classes[5][1])
    )

    for name, cls in classes:
        # --- Warmup ---
        token: str = cls.encrypt(PLAINTEXT, KEY1, KEY2)
        for _ in range(WARMUP_RUNS):
            cls.encrypt(PLAINTEXT, KEY1, KEY2)
            cls.decrypt(token, KEY1, KEY2)

        # --- Benchmark ENCRYPT ---
        encrypt_times: list[int | float] = timeit.repeat(
            stmt=lambda: cls.encrypt(PLAINTEXT, KEY1, KEY2),
            repeat=REPETICOES,
            number=EXECUCOES_POR_CICLO,
        )

        # --- Benchmark DECRYPT ---
        decrypt_times: list[int | float] = timeit.repeat(
            stmt=lambda: cls.decrypt(token, KEY1, KEY2),
            repeat=REPETICOES,
            number=EXECUCOES_POR_CICLO,
        )

        def process_stats(times) -> dict[str, float]:
            per_op_ms: list[float] = [
                (t / EXECUCOES_POR_CICLO) * 1_000_000 for t in times
            ]

            return {
                'min': min(per_op_ms),
                'mean': statistics.mean(per_op_ms),
                'stdev': statistics.stdev(per_op_ms),
            }

        e_stats: dict[str, float] = process_stats(encrypt_times)
        d_stats: dict[str, float] = process_stats(decrypt_times)

        results.append(
            [
                name,
                f'{e_stats["min"]:.4f} μs',
                f'{e_stats["stdev"]:.4f}',
                f'{d_stats["min"]:.4f} μs',
                f'{d_stats["stdev"]:.4f}',
                f'{len(cls.encrypt(PLAINTEXT, KEY1, KEY2))} chars',
                f'{asizeof.asizeof(cls.encrypt(PLAINTEXT, KEY1, KEY2))}B {asizeof.asizeof(cls.encrypt(PLAINTEXT, KEY1, KEY2)) - asizeof.asizeof(default_bytesize)}B',
            ]
        )

    headers: tuple[str, ...] = (
        'Class',
        'Encrypt (min)',
        'Enc StdDev',
        'Decrypt (min)',
        'Dec StdDev',
        'Encrypted Data Length',
        'Encrypted Bytesize',
    )

    title = f'BENCHMARK ({EXECUCOES_POR_CICLO} execs/ciclo, {REPETICOES} ciclos)'

    print('\n' + '=' * 144)
    print(f'{title:^144}')
    print('=' * 144)
    print(tabulate(results, headers=headers, tablefmt='fancy_grid'))


if __name__ == '__main__':
    run_benchmark()
