import random
from locust import HttpUser, task, between

class CacheUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def get_value(self):
        key = f"test{random.randint(1, 10000)}"
        with self.client.get(f"/get?key={key}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to get key: {key} - Status code: {response.status_code}")

    @task(1)
    def put_value(self):
        key = f"test{random.randint(1, 10000)}"
        value = "x" * 256
        with self.client.post("/put", json={"key": key, "value": value}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to put key: {key} - Status code: {response.status_code}")
