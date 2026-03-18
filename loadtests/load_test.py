"""
uv run locust -f loadtests/load_test.py --headless \
    --csv report/csv/load/load --html report/html/load.html -H http://localhost:8000
"""

from typing import Final

from locust import LoadTestShape, stats
from utils import (
    DjangoUser,
    HumanStage,
    LocustStage,
    handle_stages,
)


stats.PERCENTILES_TO_CHART = [0.5, 0.75, 0.90, 0.95, 0.99]
stats.PERCENTILES_TO_REPORT = [0.5, 0.75, 0.90, 0.95, 0.99]
stats.PERCENTILES_TO_STATISTICS = [0.5, 0.75, 0.90, 0.95, 0.99]


class WebsiteUser(DjangoUser):
    """
    This user inherits from DjangoUser, so it logs in automatically
    via on_start before starting tasks.
    """


class LoadTest(LoadTestShape):
    r"""
    Three-staged, short duration, simple loadtest profile:
    - Stage 0: 0 -> 250 users in 5 minutes
    - Stage 1: 250 users for 5 minutes
    - Stage 2: 250 -> 0 users in 5 minutes

    Test Profile:

    |===============================================================================|
    |                                                                               |
    |                  ___________________________________________                  |
    |               _-‾                                           ‾-_               |
    |            _-‾                                                 ‾-_            |
    |         _-‾                                                       ‾-_         |
    |      _-‾                                                             ‾-_      |
    |   _-‾                                                                   ‾-_   |
    |_-‾                                                                         ‾-_|
    |===============================================================================|
    """

    STAGES: Final[list[LocustStage]] = handle_stages(
        HumanStage(duration='5m', users=250, spawn_rate=5 / 6),
        HumanStage(duration='5m', users=250, spawn_rate=5 / 6),
        HumanStage(duration='5m', users=0, spawn_rate=5 / 6),
    )

    def tick(self) -> tuple[int, float] | None:
        """Função orquestradora do teste de carga"""

        run_time: float = self.get_run_time()

        for stage in self.STAGES:
            if run_time < stage['duration']:
                return (
                    stage['users'],
                    stage['spawn_rate'],
                )

        return None
