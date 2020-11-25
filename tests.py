"""
    General architecture tests
    Brief: This tests suite should be completly separated from the load balancer implementation
    and it should make just the port forwarding assumption.
"""

import requests
from endpoint_waker import EndpointWaker
import timeit

HOST = None
PORT = None
MAIN_ENDPOINT = None
REGIONS_SPECS = None
REQ_NUM = None
MAXIMUM_TIME_DEVIATION = None

def init_testing_environment(cfg):
    print('General architecture tests environment init')
    global HOST
    global PORT
    global MAIN_ENDPOINT
    global REGIONS_SPECS
    global REQ_NUM
    global MAXIMUM_TIME_DEVIATION

    HOST = cfg['host']
    PORT = cfg['port']
    MAIN_ENDPOINT = cfg['main_endpoint']
    REGIONS_SPECS = cfg['regions']
    REQ_NUM = cfg['req_num']
    MAXIMUM_TIME_DEVIATION = cfg['epsilon']

    endpoints = []
    for r in REGIONS_SPECS:
        region_name = r
        region_instances = REGIONS_SPECS[r]
        for i in range(region_instances):
            endpoint = HOST + ':' + str(PORT) + '/' + MAIN_ENDPOINT + '/' + region_name + '/' + str(i)
            endpoints.append(endpoint)

    # Wake up all instances to be sure that there are no
    # abnormal response times
    wake_up_all_instances(endpoints)

def create_endpoints():
    global HOST
    global PORT
    global MAIN_ENDPOINT
    global REGIONS_SPECS
    global REQ_NUM
    global MAXIMUM_TIME_DEVIATION

    endpoints = []
    for r in REGIONS_SPECS:
        region_name = r
        region_instances = REGIONS_SPECS[r]
        for i in range(region_instances):
            endpoint = HOST + ':' + str(PORT) + '/' + MAIN_ENDPOINT + '/' + region_name + '/' + str(i)
            endpoints.append(endpoint)
    
    return endpoints

def create_regional_endpoints():
    global HOST
    global PORT
    global MAIN_ENDPOINT
    global REGIONS_SPECS
    global REQ_NUM
    global MAXIMUM_TIME_DEVIATION

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

"""
    @return: { endpoint: max response per instance, [array with time values during test for plotting] }
    @brif: Testing policy using EMA (exponential moving average) with dynamic parameters k

"""
def requests_per_instance(cfg):
    print('Estimating maximum req number per instance')
    init_testing_environment(cfg)
    
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

"""
    @return: {region : mean latency value per region }

"""
def latency_per_region(cfg):
    print('Calculating latency per region')
    init_testing_environment(cfg)

    endpoints = create_regional_endpoints()
    latency_per_region = {}

    for endpoint in endpoints:
        latencies = []
        for i in range(REQ_NUM):

            start_time = timeit.default_timer()
            
            r = requests.get(endpoint)

            elapsed = timeit.default_timer() - start_time

            data = r.json()
            print(data)
            response_time = float(data['response_time'])
            work_time = float(data['work_time'])
            latency = response_time + work_time + elapsed
            latencies.append(latency)

        mean_latency = sum(latencies) / REQ_NUM
        region = endpoint.split('/')[-1]
        print(region)
        latency_per_region[region] = mean_latency
    
    return latency_per_region

"""
    @return: {region : mean work time value per region }

"""
def work_time_per_region(cfg):
    print('Calculating work time per region')
    init_testing_environment(cfg)
    
    endpoints = create_regional_endpoints()
    work_time_per_region = {}

    for endpoint in endpoints:
        work_times = []
        for i in range(REQ_NUM):
            r = requests.get(endpoint)
            data = r.json()
            print(data)
            work_time = float(data['work_time'])
            work_times.append(work_time)

        mean_work_time = sum(work_times) / REQ_NUM
        region = endpoint.split('/')[-1]

        work_time_per_region[region] = mean_work_time
    
    return work_time_per_region

"""
    @return: {instance : response time without load }
    @brief: The idea here is to let specific time intervals between requests
    to make sure that any instance which is tested is not loaded.
"""
def response_time_without_load(cfg):
    print('Calculating response time per worker without load')
    init_testing_environment(cfg)

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


"""
    @return: {instance : mean forward unit latency estimation }
    This function will calculate the average elapsed time for a number
    of requests for any region
"""
def forwarding_unit_latency_estiamation(cfg):
    print('Calculating forwarding unit latency per region')
    init_testing_environment(cfg)

    endpoints = create_regional_endpoints()
    forwarding_unit_latency_estiamation = {}

    for endpoint in endpoints:
        fw_latencies = []
        for i in range(REQ_NUM):

            start_time = timeit.default_timer()
            r = requests.get(endpoint)
            elapsed = timeit.default_timer() - start_time

            fw_latency = elapsed
            fw_latencies.append(fw_latency)

        mean_fw_latency = sum(fw_latencies) / REQ_NUM
        region = endpoint.split('/')[-1]

        forwarding_unit_latency_estiamation[region] = mean_fw_latency
    
    return forwarding_unit_latency_estiamation
