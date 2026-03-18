import ctypes
import gc
from sys import stdout
from typing import Any, Final

from crypt.algo import sWardenCryptography
from django import setup
from django.conf import settings


MCL_CURRENT: Final[int] = 1
MCL_FUTURE: Final[int] = 2
PR_SET_DUMPABLE: Final[int] = 4


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


def on_starting(_: Any) -> None:
    """Executed before creating workers"""

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

    stdout.write('Dealing with Garbage Collector\n')
    gc.collect()
    gc.freeze()
    stdout.flush()


# Socket
bind: str = '0.0.0.0:8000'
backlog: int = 2048
# If Nginx on the same host:
# bind: str = "unix:/run/gunicorn.sock"

# Workers
workers: int = 3  # Commented for default value using
worker_class: str = 'gthread'
threads: int = 4  # Commented for default value using

# Reliability
timeout: int = 60
keepalive: int = 5
max_requests: int = 1000
max_requests_jitter: int = 50

# Logging
loglevel: str = 'info'
accesslog: str = '-'  # Send access logs to stdout
errorlog: str = '-'  # Send error logs to stderr

# App Loading
preload_app: bool = True

# Temp Dir in-Memory
worker_tmp_dir: str = '/dev/shm'
