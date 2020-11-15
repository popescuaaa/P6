from threading import Thread, Lock
import requests

class Worker(Thread):
    def __init__(self, endpoint, req_num, idx):
        Thread.__init__(self)
        self.endpoint = endpoint
        self.req_num = req_num
        self.idx = idx
        self.status = False
        self.req_num_lock = Lock()
        self.status_lock = Lock()
    
    def run(self):
        while self.req_num:
            r = requests.get(self.endpoint)
            data = r.json()
            print('The server {} from {} solved a request'.format(data['machine'], self.endpoint.split('/')[-2]))
            self.req_num_lock.acquire()
            self.req_num -= 1
            self.req_num_lock.release()
        self.finished = True

    def get_staus(self):
        self.status_lock.acquire()
        return self.status

    def get_req_num(self):
        self.req_num_lock.acquire()
        return self.req_num

    def update_req_num(self, new_req_num):
        self.counter_lock.acquire()
        self.counter = new_req_num
        self.counter_lock.release()
