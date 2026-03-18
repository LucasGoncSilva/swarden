"""
uv run locust -f loadtests/soak_test.py --headless \
    --csv report/csv/soak/soak --html report/html/soak.html -H http://localhost:8000
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


class SoakTest(LoadTestShape):
    r"""
    Three-staged, long duration, simple loadtest profile:
    - Stage 0: 0 -> 250 users in 2 minutes
    - Stage 1: 250 users for 5 hours, 40 minutes
    - Stage 2: 250 -> 0 users in 2 minutes

    Test Profile:

    |===============================================================================|
    |                                                                               |
    |      ___________________________________________________________________      |
    |     /                                                                   \     |
    |    /                                                                     \    |
    |   /                                                                       \   |
    |  /                                                                         \  |
    | /                                                                           \ |
    |/                                                                             \|
    |===============================================================================|
    """

    STAGES: Final[list[LocustStage]] = handle_stages(
        HumanStage(duration='2m', users=250, spawn_rate=25 / 12),
        HumanStage(duration='5h40', users=250, spawn_rate=25 / 12),
        HumanStage(duration='2m', users=0, spawn_rate=25 / 12),
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
