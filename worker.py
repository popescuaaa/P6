from threading import Thread

class Worker(Thread):
    def __init__(self, endpoint, req_num):
        super().__init__(self)
        self.endpoint = endpoint
        self.req_num = req_num