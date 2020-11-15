import requests
from threading import Thread

class EndpointWaker(Thread):
    def __init__(self, endpoint):
        Thread.__init__(self)
        self.endoint = endpoint
        
    def run(self):
        r = requests.get(self.endoint)
        data = r.json()
        print('The server: {} from  {} is awake'.format(data['machine'], self.endoint.split('/')[-2]))
