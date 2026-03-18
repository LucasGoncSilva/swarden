import sys
from collections.abc import Callable, Generator
from contextlib import suppress
from functools import wraps
from itertools import compress, product
from os import getenv
from pathlib import Path
from typing import Any, Final
from uuid import uuid4

from crypt.algo import sWardenCryptography
from django.conf import settings
from django.test.runner import DiscoverRunner
from memray import FileReader, Tracker


class GlobalSetupRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs: Any) -> None:
        sys.stdout.write('Warming up sWardenCryptography algorithms:\n')
        sample: Final[str] = 'imagine-its-a-super-strong-passphrase'

        sys.stdout.write('\tWarming up Policy 1... ')
        encrypt_policy_1: str = sWardenCryptography.encrypt(
            sample,
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
            1,
        )
        sys.stdout.write('Done!\n\tWarming up Policy 2... ')
        encrypt_policy_2: str = sWardenCryptography.encrypt(
            sample,
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
            2,
        )
        sys.stdout.write('Done!\n\tWarming up Policy 3... ')
        encrypt_policy_3: str = sWardenCryptography.encrypt(
            sample,
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
            3,
        )
        sys.stdout.write('Done!\n\tWarming up Policy 4... ')
        encrypt_policy_4: str = sWardenCryptography.encrypt(
            sample,
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
            4,
        )
        sys.stdout.write('Done!\n')

        decrypt_policy_1: str = sWardenCryptography.decrypt(
            encrypt_policy_1,
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
        )
        decrypt_policy_2: str = sWardenCryptography.decrypt(
            encrypt_policy_2,
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
        )
        decrypt_policy_3: str = sWardenCryptography.decrypt(
            encrypt_policy_3,
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
        )
        decrypt_policy_4: str = sWardenCryptography.decrypt(
            encrypt_policy_4,
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
        )

        assert (
            decrypt_policy_1 == decrypt_policy_2 == decrypt_policy_3 == decrypt_policy_4
        )

        super().setup_test_environment(**kwargs)

    def teardown_test_environment(self, **kwargs: Any) -> None:
        super().teardown_test_environment(**kwargs)
        sys.stdout.flush()


def create_scenarios(params: list[dict[str, Any]]) -> Generator[Any]:
    for case in product((0, 1), repeat=len(params)):
        if all(case):
            break
        _temp: compress[dict[str, Any]] = compress(params, case)
        temp: list[dict[str, Any]] = list(_temp)
        scenario: dict = {}

        for param in temp:
            scenario.update(param)

        yield case, scenario


def limit_memory(KiB: int | float) -> Any:
    def decorator(func: Callable) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            is_coverage_active = (
                'coverage' in sys.modules or getenv('PYTEST_COV_DIR') is not None
            )
            effective_limit = KiB * 1.5 if is_coverage_active else KiB

            temp_dir: Path = Path(getenv('TMPDIR', '/tmp'))
            trace_path: Path = temp_dir / f'memray_{uuid4().hex}.bin'

            try:
                with Tracker(trace_path, native_traces=True):
                    result: Any = func(*args, **kwargs)

                reader: FileReader = FileReader(trace_path)
                peak_bytes: int = reader.metadata.peak_memory
                peak_kib: int | float = peak_bytes / 1024

                if peak_kib > effective_limit:
                    raise AssertionError(
                        'Memory limit exceeded.'
                        f'\n\tPeak: {peak_kib:.2f}KiB\n\tLimit: {effective_limit}KiB'
                        f'\n\t(Adjusted for Coverage: {is_coverage_active})'
                    )

                return result

            finally:
                if trace_path.exists():
                    with suppress(OSError):
                        trace_path.unlink()

        return wrapper

    return decorator
