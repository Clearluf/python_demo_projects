from locust import Locust, TaskSequence, seq_task, task


class MyTaskSequence(TaskSequence):
    @seq_task(1)
    def first_task(self):
        pass
 
    @seq_task(2)
    @task(2)
    def second_task(self):
        pass
 
    @seq_task(3)
    @task(5)
    def third_task(self):
        pass