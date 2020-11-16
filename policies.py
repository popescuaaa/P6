import requests
from math import exp, ceil
import least_connection_utils
import weighted_least_connection_utils
from heapq import heappush, heappop
import random

REQ_SCORE_TEST = 10
DEFAULT_COUNTER = 0

EPS = 100

'''
    This load balancing algorithm does not take into consideration the characteristics of the application 
    servers i.e. it assumes that all application servers are the same with the same availability, 
    computing and load handling characteristics.
'''
def round_robin(endpoints, req_num):
    for i in range(req_num):
        r = requests.get(endpoints[i % len(endpoints)])
        data = r.json()
        print('{} => {}'.format(data, r.elapsed))

def gather_enpoints_score(endpoints, mean_times = False):
    print('Calculating scores (and mean response time ~ latency) for each endpoint...')
    scores = {}
    times = {}
    for endpoint in endpoints:
        score_values = []
        times_values = []

        for i in range(REQ_SCORE_TEST):
            r = requests.get(endpoint)
            data = r.json()
            score_values.append(float(data['response_time']) + float(data['work_time']))
            times_values.append(float(data['response_time']))

        scores[endpoint] = score_values
        times[endpoint] = times_values

    
    # Mean
    for e in scores:
        max_score = max(scores[e])
        scores[e] = sum(scores[e]) / REQ_SCORE_TEST
        scores[e] = scores[e] / max_score
        times[e] = sum(times[e]) / REQ_SCORE_TEST

    # Trasfer data trouch softmax for creating an array of sum 1
    scores_sum = sum([exp(scores[e]) for e in scores])

    for e in scores:
        scores[e] = exp(scores[e]) / scores_sum
    if not mean_times:
        return scores
    else:
        return scores, times

'''
    Weighted Round Robin builds on the simple Round-robin load balancing algorithm to account 
    for differing application server characteristics. The administrator assigns a weight to each 
    application server based on criteria of their choosing to demonstrate the application servers 
    traffic-handling capability. If application server #1 is twice as powerful as application server #2 
    (and application server #3), application server #1 is provisioned with a higher weight and application 
    server #2 and #3 get the same weight. If there five (5) sequential client requests, the first two (2) go 
    to application server #1, the third (3) goes to application server #2, the fourth (4) to application 
    server #3 and the fifth (5) to application server #1.
'''
def weigthed_round_robin(endpoints, req_num):
    scores = gather_enpoints_score(endpoints)
    req_counter = 0
    endpoint_index = 0
    while req_counter != req_num:
        score = int(ceil(scores[endpoints[endpoint_index % len(endpoints)]]))
        for i in range(score):
            r = requests.get(endpoints[req_counter % len(endpoints)])
            data = r.json()
            print('{} => {}'.format(data, r.elapsed))
        req_counter += score
        endpoint_index += 1

'''
    Least Connection load balancing is a dynamic load balancing algorithm where client requests 
    are distributed to the application server with the least number of active connections at the 
    time the client request is received. In cases where application servers have similar specifications, 
    an application server may be overloaded due to longer lived connections; this algorithm takes the 
    active connection load into consideration.

    In this case the ideea is to split the task among a number of len(endpoints) workers who will
    perform requests each on specific endpoint and because we consider in this load balacing technique 
    that all the machines are equal we can simply rotate the batches of requests on a new set of workers.
    Why is this least connection in essence ? As we consider the working of this algoriuthm is very simple
    to show that if a thread starts at t with b requests and the others at t+i, i = 1, n-1, the server with t
    will be probabilistically the first to finish and we can then we can manage them again.
'''
def least_connection(endpoints, req_num):
    master = least_connection_utils.Master(endpoints, req_num)
    master.start()
    master.join()

'''
    Weighted Least Connection builds on the Least Connection load balancing algorithm to account for 
    differing application server characteristics. The administrator assigns a weight to each application server 
    based on criteria of their choosing to demonstrate the application servers traffic-handling capability.
    The LoadMaster is making the load balancing criteria based on active connections and application server weighting.
'''
def weighted_lest_connnection(endpoints, req_num):
    scores = gather_enpoints_score(endpoints)
    master = weighted_least_connection_utils.Master(endpoints, req_num, scores)
    master.start()
    master.join()

'''
    Fixed Weighting is a load balancing algorithm where the administrator assigns a weight to each application server 
    based on criteria of their choosing to demonstrate the application servers traffic-handling capability. 
    The application server with the highest weigh will receive all of the traffic. If the application server with the 
    highest weight fails, all traffic will be directed to the next highest weight application server.

    If the last request has a response time bigger than the average with eps (set value) then go to next endpoint.
'''
def fixed_weighting(endpoints, req_num):
    scores, times = gather_enpoints_score(endpoints, True)
    registered_endpoints = []
    for e in endpoints:
        heappush(registered_endpoints, (scores[e], e))
    
    req_counter = 0
    while True:
        if req_counter < req_num:
            score, current_endpoint = heappop(registered_endpoints)

            while req_counter < req_num:
                r = requests.get(current_endpoint)
                data = r.json()
                print('The server {} from {} solved a request'.format(data['machine'], current_endpoint.split('/')[-2]))
            
                if float(data['response_time']) > times[current_endpoint] + EPS:
                    # Create cyclic behaviour in priority queue

                    heappush(registered_endpoints, (score, current_endpoint))
                    break

                req_counter += 1
        else:
            break

'''
    Fixed Weighting is a load balancing algorithm where the administrator choose random an endpoint from 
    the list at each step.
'''
def randomized_static(endpoints, req_num):
    random.seed(42)
    req_counter = 0
    
    while req_counter < req_num:
        target = random.choice(endpoints)

        r = requests.get(target)
        data = r.json()
        print('The server {} from {} solved a request'.format(data['machine'], target.split('/')[-2]))

        req_counter += 1