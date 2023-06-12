from locust import HttpUser, task

class LoadTesting(HttpUser):
    @task
    def root_call(self):
        self.client.get("/", json={})