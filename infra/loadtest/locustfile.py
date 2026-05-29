"""Locust load test — M12: 50 concurrent users."""

from locust import HttpUser, between, task


class DomainMindUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def chat_completion(self):
        self.client.post(
            "/v1/chat/completions",
            json={
                "model": "domainmind",
                "messages": [{"role": "user", "content": "What is SOC 2 Type II?"}],
            },
            headers={"X-Model-Mode": "combined", "X-Tenant-Id": "loadtest"},
        )

    @task(1)
    def health(self):
        self.client.get("/health")
