"""
uv run locust -f loadtests/spike_test.py --headless \
    --csv report/csv/spike/spike --html report/html/spike.html -H http://localhost:8000
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


class SpikeTest(LoadTestShape):
    r"""
    Seven-staged, short duration, simple loadtest profile:
    - Stage 0: 0 -> 100 users in 10 seconds
    - Stage 1: 100 users for 1 minute
    - Stage 2: 100 -> 1500 users in 10 seconds
    - Stage 3: 1500 users for 2 minutes
    - Stage 4: 1500 -> 100 users in 10 seconds
    - Stage 5: 100 users for 15 minutes
    - Stage 6: 100 -> 0 users in 10 seconds

    Test Profile:

    |===============================================================================|
    |        __________________                                                     |
    |      ⎹                   ⎸                                                   |
    |       |                   |                                                   |
    |       ⎸                  ⎹                                                   |
    |     ⎹                      ⎸                                                 |
    |      |                     |                                                  |
    | _____⎸                    ⎹_________________________________________________ |
    |/                                                                             \|
    |===============================================================================|
    """

    STAGES: Final[list[LocustStage]] = handle_stages(
        HumanStage(duration='10s', users=100, spawn_rate=10),
        HumanStage(duration='1m', users=100, spawn_rate=10),
        HumanStage(duration='10s', users=1500, spawn_rate=140),
        HumanStage(duration='2m', users=1500, spawn_rate=140),
        HumanStage(duration='10s', users=100, spawn_rate=140),
        HumanStage(duration='15m', users=100, spawn_rate=140),
        HumanStage(duration='10s', users=0, spawn_rate=1),
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
