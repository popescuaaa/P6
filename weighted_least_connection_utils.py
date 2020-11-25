from threading import Thread, Lock
import requests
from time import sleep
from heapq import heappush, heappop

DEFAULT_NUMBER_OF_BATCHES = 10
DEFAULT_SLEEP_TIME = 5

class Master(Thread):
    def __init__(self, endpoints, req_num, scores):
        Thread.__init__(self)
        self.endpoints = endpoints
        self.scores = scores
        self.req_num = req_num
        self.workers = []
        self.worker_status_lock = Lock()
        self.registered_workers = []

        self.future_workers_idx = len(self.endpoints)

        self.batch_size = req_num // DEFAULT_NUMBER_OF_BATCHES
        self.available_workload = (DEFAULT_NUMBER_OF_BATCHES - len(endpoints))

        for idx in range(len(self.endpoints)):
            w = Worker(self.endpoints[idx], self.batch_size, idx, self.scores[self.endpoints[idx]], self)
            self.workers.append(w)

    def register_for_work(self, worker):
        self.worker_status_lock.acquire()
        heappush(self.registered_workers, (worker.score, worker))
        self.worker_status_lock.release()
        
    def delegate_new_work(self):
        if self.registered_workers != [] and len(self.registered_workers) >= 2:
            score, worker = heappop(self.registered_workers)
            self.worker_status_lock.acquire()

            print('Worker: {} requested more work with endpoint score: {}'.format(worker.idx, worker.score))
            # We must delegate the worker with a new batch of requests

            if self.available_workload > 0:
                w = Worker(worker.endpoint, self.batch_size, self.future_workers_idx, score, self)
                self.future_workers_idx += 1
                self.available_workload -= 1
                self.workers.append(w)
                w.start()
            else:
                worker.kill()
            self.worker_status_lock.release()
    
    def run(self):
        for w in self.workers:
            w.start()
        
        for w in self.workers:
            w.join()

class Worker(Thread):
    def __init__(self, endpoint, req_num, idx, score, master):
        Thread.__init__(self)
        self.endpoint = endpoint
        self.req_num = req_num
        self.idx = idx
        self.score = score
        self.master = master
        self.req_num_lock = Lock()
        self.status = None

    def run(self):
        if self.status is None:
            for i in range(self.req_num):
                    r = requests.get(self.endpoint)
                    data = r.json()
                    print('The server {} from {} solved a request managed by worker number: {}'.format(data['machine'], self.endpoint.split('/')[-2], self.idx))
            self.master.register_for_work(self)
            self.master.delegate_new_work()
        else:
            sleep(DEFAULT_SLEEP_TIME)
    
    def kill(self):
        print('Current worker: {} killed by master.'.format(self.idx))
        self.staus = 'killed'
