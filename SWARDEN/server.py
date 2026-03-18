import ctypes
import gc
from multiprocessing import set_start_method
from os import environ
from sys import stdout
from typing import Final

from crypt.algo import sWardenCryptography
from django import setup
from django.conf import settings
from granian import Granian
from granian.constants import Interfaces


MCL_CURRENT: Final[int] = 1
MCL_FUTURE: Final[int] = 2
PR_SET_DUMPABLE: Final[int] = 4


environ.setdefault('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev')


def hardening() -> None:
    try:
        libc = ctypes.CDLL('libc.so.6')

        # Prevent Swap
        if libc.mlockall(MCL_CURRENT | MCL_FUTURE) == 0:
            stdout.write('Memory locked (mlockall): SUCCESS\n')
        else:
            stdout.write('Memory locked (mlockall): FAILED (Requires CAP_IPC_LOCK)\n')

        # Prevent Memory Dumps (prctl)
        if libc.prctl(PR_SET_DUMPABLE, 0) == 0:
            stdout.write('Process non-dumpable (prctl): SUCCESS\n')
        else:
            stdout.write('Process non-dumpable (prctl): FAILED\n')

    except Exception as e:
        stdout.write(f'OS Hardening failed: {e}\n')


def warm_up() -> None:
    stdout.write("Getting Django's dependencies into memory\n")
    setup()

    stdout.write('Warming up cryptography (Generating persistent cache)...\n')
    for i in (1, 2, 3, 4):
        stdout.write(f'\tWarming policy {i}... ')
        sWardenCryptography.encrypt(
            'imagine-its-a-super-strong-passphrase',
            settings.CRYPTOGRAPHY_KEY,
            settings.SYSTEM_PEPPER,
            i,
        )
        stdout.write('OK\n')

    hardening()

    stdout.write('Freezing memory state with GC\n')
    gc.collect()
    gc.freeze()

    stdout.flush()


if __name__ == '__main__':
    set_start_method('fork')

    warm_up()

    Granian(
        target='CORE.asgi:application',
        address='0.0.0.0',
        port=8000,
        interface=Interfaces.ASGINL,
        workers=2,
        runtime_threads=4,
        blocking_threads=2,
        backlog=2048,
    ).serve()
