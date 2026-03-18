"""
uv run locust -f loadtests/stress_test.py --headless \
    --csv report/csv/stress/stress --html report/html/stress.html -H http://localhost:8000
"""

from typing import Final

from locust import LoadTestShape, stats
from utils import (
    DjangoUser,
)


stats.PERCENTILES_TO_CHART = [0.5, 0.75, 0.90, 0.95, 0.99]
stats.PERCENTILES_TO_REPORT = [0.5, 0.75, 0.90, 0.95, 0.99]
stats.PERCENTILES_TO_STATISTICS = [0.5, 0.75, 0.90, 0.95, 0.99]


class WebsiteUser(DjangoUser):
    """
    This user inherits from DjangoUser, so it logs in automatically
    via on_start before starting tasks.
    """


class StressTest(LoadTestShape):
    r"""
    Five-staged, medium duration, simple loadtest profile:
    - Stage 0: 0 -> 10 users instantly
    - Stage 1: wait 30 secs
    - Stage 2: increase 10 users instantly
    - Stage 3: check test duration against time limit
    - Stage 4: GOTO Stage 1

    Test Profile:

    |===============================================================================|
    |                                                                      _⎽⎽⎼⎼⎻⎻⎺⎺‾|
    |                                                            _⎽⎽⎼⎼⎻⎻⎺⎺‾          |
    |                                                  _⎽⎽⎼⎼⎻⎻⎺⎺‾                    |
    |                                        _⎽⎽⎼⎼⎻⎻⎺⎺‾                              |
    |                              _⎽⎽⎼⎼⎻⎻⎺⎺‾                                        |
    |                    _⎽⎽⎼⎼⎻⎻⎺⎺‾                                                  |
    |          _⎽⎽⎼⎼⎻⎻⎺⎺‾                                                            |
    |_⎽⎽⎼⎼⎻⎻⎺⎺‾                                                                      |
    |===============================================================================|
    """

    TIME_LIMIT_1_HOUR: Final[int] = 3600
    SPAWN_RATE: Final[int] = 10

    def tick(self) -> tuple[int, float] | None:
        """Função orquestradora do teste de carga"""

        run_time: float = self.get_run_time()

        if run_time < self.TIME_LIMIT_1_HOUR:
            return int(10 + (run_time // 30) * 10), self.SPAWN_RATE

        return None
