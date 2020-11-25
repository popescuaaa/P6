from load_balancer import LoadBalancer, POLICIES
from tests import *
import matplotlib.pyplot as pyplot
import yaml

if __name__ == "__main__":
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    """
        Test general architecture capabilities
    """
    # 0
    cfg = config['general_architecture']
    # 1
    # ga_rpi = 'ga_rpi.log'
    # requests_per_instance = requests_per_instance(cfg)
    # logfile = open(ga_rpi, "w")
    # for e in requests_per_instance:
    #     logfile.write('Endpoint: {} limit: {}'.format(e, requests_per_instance[e][0]))
    #     logfile.write('\n')
    # logfile.close()
    # 2
    # latency_per_region = latency_per_region(cfg)
    # ga_lpr = 'ga_lpr.log'
    # logfile = open(ga_lpr, "w")
    # for r in latency_per_region:
    #     logfile.write('Region: {} latency: {}'.format(r, latency_per_region[r]))
    #     logfile.write('\n')
    # logfile.close()
    # 3
    work_time_per_region = work_time_per_region(cfg)
    ga_wtpr = 'ga_wtpr.log'
    logfile = open(ga_wtpr, "w")
    for r in work_time_per_region:
        logfile.write('Region: {} work time: {}'.format(r, work_time_per_region[r]))
        logfile.write('\n')
    logfile.close()
    # 4
    #response_time_without_load = response_time_without_load(cfg)
    #5
    #forwarding_unit_latency_estiamation = forwarding_unit_latency_estiamation(cfg)

    """
        Test load balancer policies compare them
    """

    # load_balancer = LoadBalancer(config)
    # load_balancer.run()