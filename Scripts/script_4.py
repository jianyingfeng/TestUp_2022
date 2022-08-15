import time
from concurrent.futures import ThreadPoolExecutor


def do(**kwargs):
    print("do do do")
    print(kwargs)
    time.sleep(kwargs['t'])
    return 'done'


class ThreadPool:
    def __init__(self, workers):
        self.tasks = []
        self.workers = workers

    def add_task(self, method, **kwargs):
        print(f"to add task, method = {method}, kwargs = {kwargs}")
        self.tasks.append({method: kwargs})

    def run(self):
        future_list = []
        with ThreadPoolExecutor(self.workers) as pool:
            for task in self.tasks:
                for k, v in task.items():
                    future = pool.submit(k, **v)
                    future_list.append(future)
        for i in future_list:
            if i.result():
                print(i.result())


if __name__ == '__main__':
    a = time.time()
    pool = ThreadPool(10)
    pool.add_task(do, t=1)
    pool.add_task(do, t=2)
    pool.add_task(do, t=3)
    pool.run()
    print(time.time() - a)

    b = time.time()
    pool = ThreadPool(10)
    pool.add_task(do, t=3, a=1, b=2)
    pool.add_task(do, t=3)
    pool.add_task(do, t=3)
    pool.run()
    print(time.time() - b)