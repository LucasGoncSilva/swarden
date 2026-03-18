from typing import Any

from CORE.middlewares.logger import bind_log_data_middleware


def bind_log_data(**kwargs: Any) -> None:
    bind_log_data_middleware(**kwargs)
