import requests
from math import exp, ceil

REQ_SCORE_TEST = 10

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

def gather_enpoints_score(endpoints):
    scores = {}
    for endpoint in endpoints:
        score_values = []
        for i in range(REQ_SCORE_TEST):
            r = requests.get(endpoint)
            data = r.json()
            print('{} => {}'.format(data, r.elapsed))
            score_values.append(float(data['response_time']) + float(data['work_time']))
        scores[endpoint] = score_values
    
    # Mean and normalization
    for e in scores:
        max_value = sum(scores[e])
        scores[e] = sum(scores[e]) / REQ_SCORE_TEST
        scores[e] = scores[e] / max_value

    # Trasfer data trouch softmax for creating an array of sum 1
    scores_sum = sum([exp(scores[e]) for e in scores])

    for e in scores:
        scores[e] = exp(scores[e]) / scores_sum

    return scores

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
'''
def least_connection():
    pass

def weghted_lest_connnection():
    pass

def fixed_weighting():
    pass

def randomized_static():
    pass