from locust import HttpUser, task

SERVER_IP_ADDR = "176.99.11.243"


class LoadTestingBraniacLMS(HttpUser):
    @task
    def test_some_pages_open(self):
        # Mainapp
        self.client.get(f"http://{SERVER_IP_ADDR}/")
        self.client.get(f"http://{SERVER_IP_ADDR}/courses/")
        self.client.get(f"http://{SERVER_IP_ADDR}/contacts/")
        # self.client.get(f"http://{SERVER_IP_ADDR}/courses/1/")
        # Authapp
        self.client.get(f"http://{SERVER_IP_ADDR}/user/register/")
        self.client.get(f"http://{SERVER_IP_ADDR}/user/login/")