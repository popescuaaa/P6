import requests
from endpoint_waker import EndpointWaker

HOST = None
PORT = None
MAIN_ENDPOINT = None
REGIONS_SPECS = None
REQ_NUM = None
MAXIMUM_TIME_DEVIATION = None

def create_endpoints():
    endpoints = []
    
    for r in REGIONS_SPECS:
        region_name = r
        region_instances = REGIONS_SPECS[r]
        for i in range(region_instances):
            endpoint = HOST + ':' + str(PORT) + '/' + MAIN_ENDPOINT + '/' + region_name + '/' + str(i)
            endpoints.append(endpoint)
    
    return endpoints

def create_regional_endpoints():
    endpoints = []
    
    for r in REGIONS_SPECS:
        region_name = r
        endpoint = HOST + ':' + str(PORT) + '/' + MAIN_ENDPOINT + '/' + region_name
        endpoints.append(endpoint)
    
    return endpoints

def wake_up_all_instances(endpoints):
    wakers = []
    for e in endpoints:
        t = EndpointWaker(e)
        t.run()
    
    for w in wakers:
        w.join()

def init_testing_environment(cfg):
    HOST = cfg['host']
    PORT = cfg['port']
    MAIN_ENDPOINT = cfg['main_endpoint']
    REGIONS_SPECS = cfg['regions']
    REQ_NUM = cfg['req_num']
    MAXIMUM_TIME_DEVIATION = cfg['epsilon']
    endpoints = create_endpoints(cfg)

    # Wake up all instances to be sure that there are no
    # abnormal response times
    wake_up_all_instances(endpoints)

"""
General architecture tests
Brief: This tests suite should be completly separated from the load balancer implementation
and it should make just the port forwarding assumption.
"""

"""
    @param: cfg: configuration file
    @return: [max response per instance, [array with time values during test for plotting]]
    @brif: Testing policy using EMA (exponential moving average) with dynamic parameters
"""
def requests_per_instance():
    print('Estimating maximum req number per instance')

    requests_per_instance = {}
    endpoints = create_endpoints()

    for endpoint in endpoints:
        early_ema_time = 0.0
        time_values = []
        for i in range(REQ_NUM):
            
            r = requests.get(endpoint)
            data = r.json()
            response_time = float(data['response_time'])
            time_values.append(response_time)

            k = float(2 / (i + 1))
            current_ema_time = response_time * k + early_ema_time * (1 - k)
           
            if response_time > current_ema_time + MAXIMUM_TIME_DEVIATION:
                requests_per_instance[endpoint] = (i, time_values)
                break
            else:
                time_values.append(response_time)
                early_ema_time = current_ema_time

        print('Done with endpoint: {}'.format(endpoint))
    return requests_per_instance

def latency_per_region():
    print('Calculating latency per region')

    endpoints = create_regional_endpoints()
    latency_per_region = {}

    for endpoint in endpoints:
        latencies = []
        for i in range(REQ_NUM):
            r = requests.get(endpoint)
            data = r.json()
            response_time = float(data['response_time'])
            work_time = float(data['work_time'])
            latency = response_time + work_time

        mean_latency = sum(latencies) / REQ_NUM
        region = endpoint.split('/')[:-1]

        latency_per_region[region] = mean_latency
    
    return latency_per_region

def work_time_per_region():
    print('Calculating work time per region')

    endpoints = create_regional_endpoints()
    work_time_per_region = {}

    for endpoint in endpoints:
        work_times = []
        for i in range(REQ_NUM):
            r = requests.get(endpoint)
            data = r.json()
            work_time = float(data['work_time'])
            work_times.append(work_time)

        mean_work_time = sum(work_times) / REQ_NUM
        region = endpoint.split('/')[:-1]

        work_time_per_region[region] = mean_work_time
    
    return work_time_per_region

"""
    The idea here is to let specific time intervals between requests
    to make sure that any instance which is tested is not loaded.
"""
def response_time_without_load():
    print('Calculating response time per worker without load')

    endpoints = create_endpoints()
    response_time_without_load = {}

    for endpoint in endpoints:
        response_times = []
        for i in range(REQ_NUM):
            
            # Let sufficient time between calls
            if i % 10 == 0:
                r = requests.get(endpoint)
                data = r.json()
                response_time = float(data['response_time'])
                response_times.append(response_time)

        mean_response_time = sum(response_times) / (REQ_NUM // 10)

        response_time_without_load[endpoint] = mean_response_time
    
    return response_time_without_load


def forwarding_unit_latency_estiamation():
    pass

