import datetime

from locust import HttpUser, SequentialTaskSet, between, task

index = 0
class MyTaskSequence(HttpUser):
    @task
    class SequentialApiTasks(SequentialTaskSet):  
        login_count = 0
        wait_time = between(0, 1)  # 用户之间请求之间的等待时间（秒）  
        def on_start(self):  
            # 在测试开始时生成一个随机用户名  
            # self.username = ''.join(random.choices(string.ascii_lowercase, k=2)) + str(self.client)  
            # print(f"User {self.username} has started")  
            global index
            self.username = f'user{index}'
            index = index+1
            print(self.username)

        @task(1)  # 这是一个权重为1的任务，表示它将被执行  
        def login(self):  
            if self.login_count > 0:
                return
            # 假设登录的URL是'/login'，并且使用POST方法  
            # 你需要根据实际的登录API进行调整  
            self.client.post("/login", json={  
                "username": self.username,  
                "password": "password123"  # 这里只是一个示例，请替换为实际的密码  
            })  
            print(f"User {self.username} has logged in")
            self.login_count = self.login_count + 1
            
                

        @task(2)  # 这是一个权重为1的任务，表示它将被执行  
        def do_something(self):  
            # 假设登录的URL是'/login'，并且使用POST方法  
            # 你需要根据实际的登录API进行调整  
            self.client.post("/do_something", json={  
                "username": self.username,  
                "password": "password123"  # 这里只是一个示例，请替换为实际的密码  
            })  
            print(f"{datetime.datetime.now()} User {self.username} is doing something")