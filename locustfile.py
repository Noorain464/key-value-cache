import random
from locust import HttpUser, task, between

class CacheUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(3)
    def get_value(self):
        self.client.get(f"/get?key=test{random.randint(1,1000)}")
    
    @task(1)
    def put_value(self):
        self.client.post("/put", json={
            "key": f"test{random.randint(1,1000)}",
            "value": "x" * 256
        })
