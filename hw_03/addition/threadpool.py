import queue
from threading import Thread


class TThreadpool:
    max_queue_size = None
    queue = queue.Queue()
    workers = None
    alive = False
    task = None

    def __init__(self, max_queue_size, task):
        self.max_queue_size = max_queue_size
        self.workers = [Thread(target=self.cycle) for _ in range(max_queue_size)]
        self.task = task

    def cycle(self):
        while self.alive:
            try:
                tmp = self.queue.get(timeout=1)
                self.task(tmp)
                self.queue.task_done()
            except queue.Empty:
                print('queue is empty')

    def start(self):
        self.alive = True
        for worker in self.workers:
            worker.start()

    def stop(self):
        self.alive = False
        self.queue.join()
        for worker in self.workers:
            worker.join()

    def add_client(self, sock):
        self.queue.put(sock)
