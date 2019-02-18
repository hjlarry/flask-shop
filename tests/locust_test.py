from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    def on_start(self):
        self.index()

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def about(self):
        self.client.get("/page/about")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://127.0.0.1:5000"
    min_wait = 1000
    max_wait = 5000
