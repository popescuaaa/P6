import requests
from endpoint_waker import EndpointWaker
"""
General architecture tests
Brief: This tests suite should be completly separated from the load balancer implementation
and it should make just the port forwarding assumption.
"""
def create_endpoints(cfg):
    endpoints = []
    host = cfg['host']
    port = cfg['port']
    main_endpoint = cfg['endpoint']
    regions_specs = cfg['regions']
    
    for r in regions_specs:
        region_name = r
        region_instances = regions_specs[r]
        for i in range(region_instances):
            endpoint = host + ':' + str(port) + '/' + main_endpoint + '/' + region_name + '/' + str(i)
            endpoints.append(endpoint)
    
    return endpoints

def wake_up_all_instances(endpoints):
    wakers = []
    for e in endpoints:
        t = EndpointWaker(e)
        t.run()
    
    for w in wakers:
        w.join()

"""
    @param: cfg: configuration file
    @return: [max response per instance]
    @brif: Testing policy using EMA (exponential moving average) with dynamic parameters
"""
def requests_per_instance(cfg):
    requests_per_instance = {}
    endpoints = create_endpoints(cfg)
    req_num = cfg['req_num']
    maximum_time_deviation = cfg['epsiolon']

    # Wake up all instances to be sure that there are no
    # abnormal response times
    wake_up_all_instances(endpoints)

    for endpoint in endpoints:
        early_ema_time = 0.0
        ema_time_values = []
        for i in range(req_num):
            
            r = requests.get(endpoint)
            data = r.json()
            time = float(data['response_time'])

            k = float(2 / (i + 1))
            current_ema_time = time * k + early_ema_time * (1 - k)
            
            if time > current_ema_time + maximum_time_deviation:
                requests_per_instance[endpoint] = (i, ema_time_values)
                break
            else:
                ema_time_values.append(early_ema_time)
                early_ema_time = current_ema_time
    
    return requests_per_instance


            

def latency_per_instance():
    pass

def work_time_instance():
    pass

def response_time_without_load():
    pass

def forwarding_unit_latency_estiamation():
    pass

