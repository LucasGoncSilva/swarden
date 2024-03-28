"""
locust --headless -f loadtests/soak_test.py -H http://localhost:8000 --processes -1 --csv report/cvs/soak/soak --html report/html/soak.html
"""

from locust import FastHttpUser, LoadTestShape, TaskSet, constant, task

from utils import handle_stages


class UserTasks(TaskSet):
    @task
    def get_root(self):
        self.client.get("/")


class WebsiteUser(FastHttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]


class SoakTest(LoadTestShape):
    stages = [
        {"duration": '2m', "users": 200, "spawn_rate": 10 / 3},
        {"duration": '5h40', "users": 200, "spawn_rate": 10 / 3},
        {"duration": '2m', "users": 0, "spawn_rate": 10 / 3},
    ]

    def tick(self):
        run_time = self.get_run_time()

        stages = handle_stages(self.stages.copy())

        for stage in stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
