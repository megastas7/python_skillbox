from queue import PriorityQueue
from threading import Thread
import time


class Producer(Thread):
    def __init__(self, tasks, queue):
        super().__init__()
        self.tasks = tasks
        self.queue = queue

    def run(self):
        print("Producer: Running")
        for task in self.tasks:
            self.queue.put(task)
            print(f">running Task(priority={task[0]}). sleep({task[1]})")
        print("Producer: Done")


class Consumer(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Consumer: Running")
        while not self.queue.empty():
            task = self.queue.get()
            priority, sleep_time = task
            time.sleep(sleep_time)
            print(f">take Task(priority={priority}). sleep({sleep_time})")
            self.queue.task_done()
        print("Consumer: Done")


queue = PriorityQueue()


tasks = [
    (0, 0.019658567230089852),
    (0, 0.8260261640443046),
    (1, 0.5049788914608555),
    (1, 0.9939451305978486),
    (2, 0.6217303299399963),
    (2, 0.7283236739267553),
    (3, 0.13090364153051426),
    (3, 0.21140406953974167),
    (4, 0.8426715099235477),
    (6, 0.43248434769420785)
]

producer = Producer(tasks, queue)
consumer = Consumer(queue)

consumer.start()
consumer.join()
producer.start()
producer.join()
