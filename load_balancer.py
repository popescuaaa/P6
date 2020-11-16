from policies import *
from endpoint_waker import EndpointWaker
import yaml

POLICIES = ['round robin', 'weighted round robin', 'least connection', 'weighted least connection', 'fixed weighting', 'randomized static']
MAX_ARGUMENTS = 2
NUMBER_OF_REQUESTS_IDX = 1

class LoadBalancer():
    def __init__(self, cfg):
        self.host = cfg['host']
        self.port = cfg['port']
        self.main_endpoint = cfg['main_endpoint']
        self.policy = cfg['policy']
        self.hosts_configuration = cfg['hosts_configuration']
        self.req_num = cfg['req_num']
        
        self.endpoints = []
        # Configure the hosts
        for e in self.hosts_configuration:
            for i in range(self.hosts_configuration[e]):
                endpoint = self.host + ':' + str(self.port) + '/' + self.main_endpoint + '/' + e + '/' + str(i)
                self.endpoints.append(endpoint)
        
        print(self.endpoints)
        if self.policy not in POLICIES:
            print('The policy is not supported. Try one of the following: {}'.format(POLICIES))
            return

        # If the servers are not awake the time for response will be abnormal
        # and one solution for this is to make a request on each of them in the 
        # beginning and then 'listen' to other requests => this task can be performed
        # in parallel for each endpoint
        wakers = []
        for e in self.endpoints:
            t = EndpointWaker(e)
            t.run()
        
        for w in wakers:
            w.join()

    def run(self):
        if self.policy == POLICIES[0]:
            round_robin(self.endpoints, self.req_num)
        elif self.policy == POLICIES[1]:
            weigthed_round_robin(self.endpoints, self.req_num)
        elif self.policy == POLICIES[2]:
            least_connection(self.endpoints, self.req_num)
        elif self.policy == POLICIES[3]:
            weighted_lest_connnection(self.endpoints, self.req_num)
        elif self.policy == POLICIES[4]:
            fixed_weighting(self.endpoints, self.req_num)
        elif self.policy == POLICIES[5]:
            randomized_static(self.endpoints, self.req_num)
if __name__ == "__main__":
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    load_balancer = LoadBalancer(config)
    load_balancer.run()
    